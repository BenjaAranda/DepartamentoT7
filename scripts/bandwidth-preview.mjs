// Local validation proxy: one shared 50 Mbps budget, no HTTP cache, no compression.
// Run while the compiled application listens on 127.0.0.1:3001.
import http from 'node:http';
import {appendFileSync} from 'node:fs';
const budget=50_000_000/8,queue=[];let credit=0,last=performance.now();
setInterval(()=>{
 const now=performance.now();credit=Math.min(budget*.02,credit+(now-last)*budget/1000);last=now;
 while(queue.length&&credit>=1){const item=queue.shift();if(item.res.destroyed)continue;
  const length=Math.min(Math.floor(credit),16384,item.body.length-item.offset);
  item.res.write(item.body.subarray(item.offset,item.offset+length));item.offset+=length;credit-=length;
  if(item.offset===item.body.length){item.res.end();appendFileSync('../work/network-50mbps.jsonl',JSON.stringify({path:item.path,bytes:item.body.length,ms:performance.now()-item.started})+'\n');}
  else queue.push(item);
 }
},5).unref();
http.createServer((req,res)=>{
 const started=performance.now();const headers={...req.headers,host:'127.0.0.1:3001','accept-encoding':'identity'};
 delete headers['if-none-match'];delete headers['if-modified-since'];
 const upstream=http.request({hostname:'127.0.0.1',port:3001,path:req.url,method:req.method,headers},response=>{
  const chunks=[];response.on('data',chunk=>chunks.push(chunk));response.on('end',()=>{
   const body=Buffer.concat(chunks),out={...response.headers,'cache-control':'no-store','content-length':String(body.length)};
   delete out.etag;delete out['last-modified'];delete out['transfer-encoding'];
   res.writeHead(response.statusCode,out);
   if(!body.length){res.end();return;}queue.push({res,body,offset:0,path:req.url,started});
  });
 });upstream.on('error',()=>{res.writeHead(502);res.end('Preview is unavailable.');});req.pipe(upstream);
}).listen(3002,'127.0.0.1',()=>console.log('50 Mbps aggregate preview: http://127.0.0.1:3002'));
