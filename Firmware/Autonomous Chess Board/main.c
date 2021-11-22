#include <msp430.h> 
#include <stdbool.h>

//FLAGS
volatile unsigned int UPFLAG = 0 ;
volatile unsigned int RIGHTFLAG = 0;
volatile unsigned int DOWNFLAG = 0;
volatile unsigned int LEFTFLAG = 0;
volatile unsigned int MOVINGFLAG = 0;
volatile unsigned int ENQUEUEFLAG = 0;
volatile unsigned int FULLFLAG = 0;
volatile unsigned int EMPTYFLAG = 0;



//PWM
volatile unsigned int steppingSpeed = 18800;
volatile unsigned int PWMStepperMax = 1880;
volatile unsigned int PWMStepperTrigger = 1015;


//stepper motor
volatile unsigned int leftMotorCW = 0;
volatile unsigned int rightMotorCW = 0;

//Queue Implementation
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

    //-------set up timer TB2 for stepper motor PWM
	//TB2 Global controls
	TB2CTL |= MC__UP;

	//setting up TB2.0 Pin 2.0
	P2DIR |= BIT0;
	P2SEL1 &= ~(BIT0);
	P2SEL0 |= BIT0;

	//setting up TB2.1 Pin 2.1
	P2DIR |= BIT1;
    P2SEL1 &= ~(BIT1);
    P2SEL0 |= BIT1;

	//setting up TB2.1 Pin 3.6
    P3DIR |= BIT6;
    P3SEL1 &= ~(BIT6);
    P3SEL0 |= BIT6;

	//setting up TB2.2 Pin 3.7
    P3DIR |= BIT7;
    P3SEL1 &= ~(BIT7);
    P3SEL0 |= BIT7;


	//set up timer TB0 for stepper motor speed

	//----------------------UART-GreenBoard-----------------//

    //Configure ports for UCA1
    P2SEL0 &= ~(BIT5 + BIT6);
    P2SEL1 |= BIT5 + BIT6;

    //Configure UCA1
    UCA1CTLW0 = UCSSEL0;
    UCA1BRW = 52;
    UCA1MCTLW = 0x4900 + UCOS16 + UCBRF0;
    UCA1IE |= UCRXIE; //receive interrupt

	//---------------------------Buffer---------------------//
	Queue buffer;
	initialize(&buffer);

	//----------------------INTERRUPTS----------------------//


	//--------------Game Start up-----------------//



	//-------------Move in direction code------------//





	return 0;
}
