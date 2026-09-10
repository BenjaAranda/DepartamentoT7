'use client';
import dynamic from 'next/dynamic';
const Simulator = dynamic(() => import('@/components/t7/simulator'), {
  ssr: false,
  loading: () => <main className="grid min-h-svh place-items-center">Preparando DepartamentoT7…</main>,
});
export default function Home() { return <Simulator />; }
