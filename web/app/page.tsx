import { Empty, EmptyDescription, EmptyHeader } from '@/components/ui/empty';

export default function Home() {
  return (
    <main className="flex min-h-svh flex-col">
      <header className="border-b border-border px-6 py-5 sm:px-10">
        <p className="text-sm font-medium text-muted-foreground">
          Los Altos de Algarrobo
        </p>
        <h1 className="mt-1 text-xl font-semibold tracking-tight">
          Departamento Tipo T7
        </h1>
      </header>
      <Empty className="rounded-none px-6 py-16">
        <EmptyHeader>
          <h2 className="text-lg font-medium">Recorrido en preparación</h2>
          <EmptyDescription className="text-base">
            El modelo del departamento todavía no está disponible.
          </EmptyDescription>
        </EmptyHeader>
      </Empty>
    </main>
  );
}
