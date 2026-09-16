// The static entry supplies <base>; the existing Sites entry resolves from /.
export function publicAsset(path: string): string {
  return new URL(path.replace(/^\/+/, ''), document.baseURI).href;
}
