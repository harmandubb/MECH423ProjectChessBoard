using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using ChessboardMovement;

namespace ChessboardMovement
{
	public partial class Form1 : Form
	{

		Board board;
		Solenoid solenoid;
		List<byte[]> UARTCommands = new List<byte[]>();

		double timerInterval = 0.5;
		int timerCounter = 0;
		double countsToWait = 10 / 0.5;

		public Form1()
		{
			InitializeComponent();
			board = new Board();
			solenoid = new Solenoid();
			
				
		}

		private void btnSubmit_Click(object sender, EventArgs e)
		{

			string origin = txtOrigin.Text;
			string destination = txtDestination.Text;

			UARTCommands.AddRange(ChessInterface.move(origin, destination, solenoid, board));
		}

		private void timer1_Tick(object sender, EventArgs e)
		{
			int numCommandsTosend = 0;

			if(timerCounter == countsToWait)
			{
				//only transmit 10 commands at a time due to firmware buffer limitation
				if (UARTCommands.Count > 0)
				{
					if (UARTCommands.Count > 10)
					{
						numCommandsTosend = 10;
					}
					else
					{
						numCommandsTosend = UARTCommands.Count;
					}

					timerCounter = 0;

					for (int i = 0; i < numCommandsTosend; i++)
					{
						if (serialPort1.IsOpen)
						{
							//sending a command
							serialPort1.Write(UARTCommands[0], 0, 3);
						}

						//ensuring that the command is deleted
						UARTCommands.RemoveAt(0);
					}

				}

			}
			timerCounter++;
		}
	}
}
