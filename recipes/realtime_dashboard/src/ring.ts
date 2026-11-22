// Fixed-capacity ring buffer: memory is allocated once, the oldest sample is overwritten.
export class RingBuffer {
  readonly values: Float64Array;
  head = 0; // index of the next write
  size = 0;

  constructor(capacity: number) {
    this.values = new Float64Array(capacity);
  }

  push(value: number): void {
    this.values[this.head] = value;
    this.head = (this.head + 1) % this.values.length;
    this.size = Math.min(this.size + 1, this.values.length);
  }

  // Copy samples oldest-first into a caller-owned array, so drawing allocates nothing.
  copyInto(out: Float64Array): number {
    const cap = this.values.length;
    const start = (this.head - this.size + cap) % cap;
    for (let i = 0; i < this.size; i++) out[i] = this.values[(start + i) % cap]!;
    return this.size;
  }
}
