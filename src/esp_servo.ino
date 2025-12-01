// #include <Servo.h>

// Servo horizontalServo; // 360° continuous rotation
// Servo verticalServo;   // 0–180 servo

// // Pins
// const int H_PIN = D1;
// const int V_PIN = D2;

// // Vertical positions
// const int V_FLAT = 30;
// const int V_UP = 180;

// // Spin timing
// const int SHORT_SPIN = 500; // recyclable & organic
// const int LONG_SPIN = 800;  // hazardous & non-recyclable

// void setup()
// {
//     Serial.begin(115200);
//     Serial.setTimeout(10);

//     horizontalServo.attach(H_PIN);
//     verticalServo.attach(V_PIN);

//     horizontalServo.write(90); // stop
//     verticalServo.write(V_FLAT);

//     Serial.println("ESP8266 Ready (USB serial mode)");
// }

// void loop()
// {
//     if (Serial.available())
//     {
//         int category = Serial.parseInt();

//         if (category >= 1 && category <= 4)
//         {
//             Serial.print("Received category: ");
//             Serial.println(category);
//             sortTrash(category);
//         }
//     }
// }

// void sortTrash(int cat)
// {

//     // ---------------------------
//     // 1. Move horizontal FIRST
//     // ---------------------------
//     if (cat == 1)
//     { // Recyclable
//         Serial.println("→ Rotate LEFT (short)");
//         spinLeft(SHORT_SPIN);
//     }
//     else if (cat == 2)
//     { // Organic
//         Serial.println("→ Rotate RIGHT (short)");
//         spinRight(SHORT_SPIN);
//     }
//     else if (cat == 3)
//     { // Hazardous
//         Serial.println("→ Rotate LEFT (long)");
//         spinLeft(LONG_SPIN);
//     }
//     else if (cat == 4)
//     { // Non-recyclable
//         Serial.println("→ Rotate RIGHT (long)");
//         spinRight(LONG_SPIN);
//     }

//     // STOP rotation after move
//     horizontalServo.write(90);
//     delay(200);

//     // ---------------------------
//     // 2. Lift up → drop trash
//     // ---------------------------
//     Serial.println("→ Lifting platform UP...");
//     verticalServo.write(V_UP);
//     delay(1200);

//     // ---------------------------
//     // 3. Lower platform
//     // ---------------------------
//     Serial.println("→ Returning platform DOWN...");
//     verticalServo.write(V_FLAT);
//     delay(1200);

//     Serial.println("✓ Sort Complete\n");
// }

// // ===========================================
// // 360° continuous servo control
// // ===========================================
// void spinLeft(int ms)
// {
//     horizontalServo.write(0); // full speed left
//     delay(ms);
//     horizontalServo.write(90); // STOP
// }

// void spinRight(int ms)
// {
//     horizontalServo.write(180); // full speed right
//     delay(ms);
//     horizontalServo.write(90); // STOP
// }