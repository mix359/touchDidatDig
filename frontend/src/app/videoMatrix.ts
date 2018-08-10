export class VideoMatrix {
    readonly id: number;
    readonly name: string;

    comunicationError: boolean = false;
    channel: number = 0;

    constructor(id: number, name: string) {
        this.id = id;
        this.name = name;
    }
}