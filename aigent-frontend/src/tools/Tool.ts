export abstract class Tool {
  abstract run(): Promise<string>;
}
