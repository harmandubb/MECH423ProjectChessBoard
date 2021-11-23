#include <msp430.h> 
#include <stdbool.h>

#define ROW_SIZE (8u)
#define COLUMN_SIZE (5u)

//FLAGS
volatile unsigned int UPFLAG = 0 ;
volatile unsigned int RIGHTFLAG = 0;
volatile unsigned int DOWNFLAG = 0;
volatile unsigned int LEFTFLAG = 0;
volatile unsigned int ENQUEUEFLAG = 0;
volatile unsigned int FULLFLAG = 0;
volatile unsigned int EMPTYFLAG = 0;
volatile unsigned int DONEMOVING = true;



//PWM
volatile unsigned int steppingSpeed = 18800;
volatile unsigned int PWMStepperMax = 1880;
volatile unsigned int PWMStepperTrigger = 1015;


//stepper motor
volatile unsigned int leftMotorCW = true;
volatile unsigned int rightMotorCW = true;
volatile int leftMotorStepState = 0;
volatile int rightMotorStepState = 0;
volatile int cyclesForHalfSquare = 236;
volatile int cycleCountsLeft = 0;

//decode variables
volatile int directionByte = -1;
volatile int solenoidByte = -1;
volatile int currentDirection = -1;


//Queue Implementation
unsigned int RxByte;
int BUFFER_SIZE = 50;

typedef struct {
    int front;
    int num;
    int capacity;
    int* arr;
} Queue;

void initialize(Queue* q) {
    q->front = 0;
    q->num = 0;
    q->capacity = BUFFER_SIZE;
    q->arr = (int*)malloc(q->capacity * sizeof(int));
}

int isEmptry(Queue* q) {
    if (q->num == 0) {
        EMPTYFLAG = 1;
        return true;
    }
    else
    {
        return false;
    }

}

int isFull(Queue* q) {
    if (q->num == q->capacity) {
        FULLFLAG = 1;
        return true;
    }
    else
        return false;
}

int enqueue(Queue* q, int val) {

    if (isFull(q))
        return false;
    else
    {
        q->arr[(q->front + q->num) % q->capacity] = val;
        q->num++;
        return true;
    }
}

int dequeue(Queue* q)
{
    int result = 0;
    if (isEmptry(q))
        return false;
    else
    {
        result = q->arr[q->front];
        q->arr[q->front] = 0;
        q->front = (q->front + 1) % q->capacity;
        q->num--;
        return result;
    }
}

static const int stepperMotorLookupTable[ROW_SIZE][COLUMN_SIZE] =
{
 {1, 0, 0, 0},      //0
 {1, 0, 1, 0},      //1
 {0, 0, 1, 0},      //2
 {0, 1, 1, 0},      //3
 {0, 1, 0, 0},      //4
 {0, 1, 0, 1},      //5
 {0, 0, 0, 1},      //6
 {1, 0, 0, 1}       //7
};
int main(void)
{
	WDTCTL = WDTPW | WDTHOLD;	// stop watchdog timer
	

	//---------------Initialization----------------//

	//----------------------CLOCK--------------------------//

    //Configure clock
    CSCTL0 = CSKEY;                                            // Write password to modify CS registers
    CSCTL1 |= DCOFSEL1 + DCOFSEL0;                              // 8 MH DCO
    CSCTL2 |= SELS0 + SELS1 + SELM0 + SELM1 + SELA0 + SELA1;    //assigning to all clocks
    CSCTL3 &= ~(DIVS2 + DIVS1 + DIVS0);                          // SMCLOCK divider is 1

    //output the smclk to P3.4
    P3DIR |= BIT4;
    P3SEL1 |= BIT4;
    P3SEL0 |= BIT4;
    //the clock is working
    //---------------------------Stepper motors------------//

    //setting up output pins
    P3DIR |= BIT0 + BIT1 + BIT2 + BIT3 + BIT4 + BIT5 + BIT6 + BIT7;
    P3SEL1 &= ~(BIT0 + BIT1 + BIT2 + BIT3 + BIT4 + BIT5 + BIT6 + BIT7);
    P3SEL0 &= ~(BIT0 + BIT1 + BIT2 + BIT3 + BIT4 + BIT5 + BIT6 + BIT7);

    //-------------------------------setting up Timer A0 for timing the system
    TA0CTL &= ~(TASSEL1 + TASSEL0);
    TA0CTL |= TASSEL1;//set the Timer source to SMCLK

    TA0CTL &= ~(ID0 + ID1);
    //TA0CTL |= ID0 + ID1; //diving by 8

    //setting time to UP mode
    TA0CTL &= ~(MC0 + MC1);
    TA0CTL |= MC__UP;

//    //setting up TA0.1
//    P1DIR |= BIT0;
//    P1SEL1 &= ~(BIT0);
//    P1SEL0 |= BIT0;
//
//    //setting the register to toggle reset mode
//    TA0CCTL1 &= ~(OUTMOD2 + OUTMOD1 + OUTMOD0);
//    TA0CCTL1 |= OUTMOD1;

    //setting compare values
    TA0CCR0 = steppingSpeed;


    //--------------------------------setting up Timer B0
    TB0CTL &= ~(TBSSEL1 + TBSSEL0);
    TB0CTL |= TBSSEL1;//set the Timer source to SMCLK

    TB0CTL &= ~(CNTL0 + CNTL1); //counter set to 16 bits

    //setting up the dividers
    TB0CTL &= ~(ID0 + ID1); //clearing dividers
    //TB0CTL |= ID0; // factor of 2 divider

    TB0EX0 &= ~(TBIDEX0 + TBIDEX1 + TBIDEX2); //clearing dividers
    //TB0EX0 |= TBIDEX0 + TBIDEX1; // factor of 4 divider

    //setting time to continuous mode
    TB0CTL &= ~(MC0 + MC1);
    TB0CTL |= MC__UP;

    //setting up TB0.1
    P1DIR |= BIT4;
    P1SEL1 &= ~(BIT4);
    P1SEL0 |= BIT4;

    //Setting TB0.1 to toggle reset mode
    TB0CCTL1 &= ~(OUTMOD2 + OUTMOD1 + OUTMOD0);
    TB0CCTL1 |= OUTMOD1;

    //setting compare values
    TB0CCR1 = PWMStepperTrigger;
    TB0CCR0 = PWMStepperMax;
    TB0R = 0xFFFF;
	//----------------------UART-RedBoard-----------------//

    //Configure ports for UCA0
    P2SEL0 &= ~(BIT0 + BIT1);
    P2SEL1 |= BIT0 + BIT1;

    // Configure UCA0
    UCA0CTLW0 = UCSSEL0; //selects UCLK clock as source for USCI_A
    UCA0BRW = 52;
    UCA0MCTLW = 0x4900 + UCOS16 + UCBRF0;
    UCA0IE |= UCRXIE;

	//---------------------------Buffer---------------------//
	Queue buffer;
	initialize(&buffer);

	Queue directions;
	initialize(&directions);

	//----------------------INTERRUPTS----------------------//
	//enable interrupt for timer A0
    TA0CTL |= TAIE;
    //enable compare and capture TA0.0 interrupt
    TA0CCTL0 |= CCIE;

    // global interrupt enable
    _EINT();

    while(true){
        //--------------Game Start up-----------------//






        //-------------Move in direction code------------//

        if(DONEMOVING){
            DONEMOVING = false;
            currentDirection = dequeue(&directions);

            if(currentDirection == 0){
                UPFLAG = 1;
            }else if(currentDirection == 1){
                RIGHTFLAG = 1;
            }else if(currentDirection == 2){
                DOWNFLAG = 1;
            }else if(currentDirection == 3){
                LEFTFLAG = 1;
            }

            cycleCountsLeft = cyclesForHalfSquare;
        }

        if(UPFLAG){
            UPFLAG = 0;
            leftMotorCW = false;
            rightMotorCW = true;
        }
        if(DOWNFLAG){
            DOWNFLAG = 0;
            leftMotorCW = true;
            rightMotorCW = false;
        }
        if(RIGHTFLAG){
            RIGHTFLAG = 0;
            leftMotorCW = false;
            rightMotorCW = false;
        }
        if(LEFTFLAG){
            LEFTFLAG = 0;
            leftMotorCW = true;
            rightMotorCW = true;
        }

        //---------------LEFT MOTOR--------------------//
        if (leftMotorStepState >= 8) {
        leftMotorStepState = 0;
        }
        else if (leftMotorStepState <= -1) {
            leftMotorStepState = 7;
        }

        if (stepperMotorLookupTable[leftMotorStepState][0] == 1) {
            P3OUT |= BIT3;
        }else{
            P3OUT &= ~BIT3;
        }
        if (stepperMotorLookupTable[leftMotorStepState][1] == 1){
            P3OUT |= BIT2;
        }else{
            P3OUT &= ~BIT2;
        }
        if (stepperMotorLookupTable[leftMotorStepState][2] == 1){
            P3OUT |= BIT1;
        }else{
            P3OUT &= ~BIT1;
        }
        if (stepperMotorLookupTable[leftMotorStepState][3] == 1){
            P3OUT |= BIT0;
        }else{
            P3OUT &= ~BIT0;
        }

        //-------------------RIGHT MOTOR------------------//
        if (rightMotorStepState >= 8) {
           rightMotorStepState = 0;
                        }
        else if (rightMotorStepState <= -1) {
            rightMotorStepState = 7;
        }

        if (stepperMotorLookupTable[rightMotorStepState][0] == 1) {
            P3OUT |= BIT7;
        }else{
            P3OUT &= ~BIT7;
        }
        if (stepperMotorLookupTable[rightMotorStepState][1] == 1){
            P3OUT |= BIT6;
        }else{
            P3OUT &= ~BIT6;
        }
        if (stepperMotorLookupTable[rightMotorStepState][2] == 1){
            P3OUT |= BIT5;
        }else{
            P3OUT &= ~BIT5;
        }
        if (stepperMotorLookupTable[rightMotorStepState][3] == 1){
            P3OUT |= BIT4;
        }else{
            P3OUT &= ~BIT4;
        }

        //--------------ENQUEUE DATA-----------------//
        if (ENQUEUEFLAG == 1) {
            ENQUEUEFLAG = 0;
            enqueue(&buffer, RxByte);
        }

        if ((buffer.num) >= 5) {
            decode(buffer,directions);
        }

    }
	return 0;
}

#pragma vector = TIMER0_A0_VECTOR
__interrupt void TIMER0_A0_ISR(void) {
    TA0IV = 0; //clear inttrupt
    TA0CCTL0 &= ~(CCIFG); //clear flag

    //have not checked if the directions works out
    if(leftMotorCW){
        leftMotorStepState++;
    } else{
        leftMotorStepState--;
    }
    if(rightMotorCW){
        rightMotorStepState++;
    } else{
        rightMotorStepState--;
    }


}

#pragma vector = USCI_A0_VECTOR
__interrupt void USCI_A0_ISR(void)
{
    RxByte = UCA0RXBUF;
    while ((UCA0IFG & UCTXIFG) == 0);
    UCA0TXBUF = RxByte;//for debugging

    ENQUEUEFLAG = 1;
}

int decode(Queue* buffer, Queue* directions){
    if (dequeue(buffer) == 255) {
        directionByte = dequeue(buffer);
        solenoidByte = dequeue(buffer);

        //store directionByte
        enqueue(directions, directionByte);

        return true;
    }

    return false;
}
