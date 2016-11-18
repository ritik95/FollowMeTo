void setup() 
{
  DDRB = 0;
  DDRB |= (1<<1);
  TCCR1A = 0;
  TCCR1B = 0;
  TCCR1C = 0;
  TCCR1A |= 1<<WGM11 | 1<<COM1A1;
  TCCR1B |= 1<<WGM12 | 1<<WGM13 | 1<<CS11;
  ICR1 = 39999;
  OCR1A = 3000;
  Serial.begin(9600); 
}
//int oc = 3000;
int angle = 90;
void servo_angle(int a)
{
  int b = (16*a) + 1500;
  OCR1A = b;
  _delay_ms(50);
}
void loop() 
{
  int x=0,y;
  if(Serial.available())
  {
    x = Serial.read();
    x = 10*x;
    y = (x - 320)/32;
    angle -= y; 
  }
  servo_angle(angle);
}
