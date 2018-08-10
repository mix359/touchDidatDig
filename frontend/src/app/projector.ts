export class Projector {
    readonly id: number;
    readonly name: string;

    comunicationError: boolean = false;
    powered: boolean = false;
    freezed: boolean = false;
    muted: boolean = false;
    blanked: boolean = false;
    source: number = 0;
    vol: number = 0;

    constructor(id: number, name: string) {
        this.id = id;
        this.name = name;
    }

}