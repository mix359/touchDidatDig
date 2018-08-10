import { TestBed, inject } from '@angular/core/testing';

import { MqttComService } from './mqtt-com.service';

describe('MqttComService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [MqttComService]
    });
  });

  it('should be created', inject([MqttComService], (service: MqttComService) => {
    expect(service).toBeTruthy();
  }));
});
