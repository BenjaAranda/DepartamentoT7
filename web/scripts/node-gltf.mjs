// Structural GLB checks need image dimensions, not a browser GPU rasterizer.
// Actual material rendering is verified separately in the browser.
globalThis.self=globalThis;
globalThis.createImageBitmap=async blob=>{
 const bytes=Buffer.from(await blob.arrayBuffer());
 if(bytes.readUInt32BE(0)!==0x89504e47)throw new Error('Validation image decoder expects PNG');
 return {width:bytes.readUInt32BE(16),height:bytes.readUInt32BE(20),close(){}};
};
