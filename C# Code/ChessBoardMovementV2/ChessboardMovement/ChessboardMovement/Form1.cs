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
using System.Collections.Concurrent;

namespace ChessboardMovement
{
	public partial class Form1 : Form
	{

		Board board;
		Solenoid solenoid;
		List<byte[]> UARTCommands = new List<byte[]>();


		double timerInterval = 0.5;
		int timerCounter = 0;
		double countsToWait = 10;
		//Class Variables
		String serialDataString = "";
		ConcurrentQueue<Int32> dataQueue = new ConcurrentQueue<Int32>();

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
			int byteData = 0;
			if (serialPort1.IsOpen)
			{
				//txtSerialBytes.Text = serialPort1.BytesToRead.ToString();
				while (dataQueue.Count != 0)
				{
					if (dataQueue.TryDequeue(out byteData))
					{
						txtSerialBytes.AppendText(Convert.ToString(byteData) + ",");
					}
					else MessageBox.Show("Dequeueing failed");
				}
			}
			int numCommandsTosend = 0;

			if (timerCounter >= countsToWait)
			{
				//only transmit 10 commands at a time due to firmware buffer limitation
				if (UARTCommands.Count > 0)
				{
					if (UARTCommands.Count > 6)
					{
						numCommandsTosend = 6;
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
							//MessageBox.Show("Sent");
						}

						//ensuring that the command is deleted
						UARTCommands.RemoveAt(0);
					}

				}

			}
			timerCounter++;
		}

		private void btnConnectDisconnect_Click(object sender, EventArgs e)
		{
			//Connect
			if (btnConnectDisconnect.Text == "Connect Serial")
			{
				btnConnectDisconnect.Text = "Disconnect Serial";

				if (serialPort1.IsOpen == true)
				{
					serialPort1.Close();
				}
				serialPort1.Open();

			}
			else if (btnConnectDisconnect.Text == "Disconnect Serial")
			{
				btnConnectDisconnect.Text = "Connect Serial";

				if (serialPort1.IsOpen == true)
				{
					serialPort1.Close();
				}

			}
		}

		private void Form1_Load(object sender, EventArgs e)
		{
			//Code segment for the computer to automatically find the comm port
			comboBoxCOMPorts.Items.Clear();
			comboBoxCOMPorts.Items.AddRange(System.IO.Ports.SerialPort.GetPortNames());
			if (comboBoxCOMPorts.Items.Count == 0)
				comboBoxCOMPorts.Text = "No COM ports!";
			else
				comboBoxCOMPorts.SelectedIndex = 0;

		}

		private void PortDataReceived(object sender, System.IO.Ports.SerialDataReceivedEventArgs e)
		{
			int newByte = 0;
			int bytesToRead;
			bytesToRead = serialPort1.BytesToRead;

			while (bytesToRead != 0)
			{
				newByte = serialPort1.ReadByte();
				dataQueue.Enqueue(newByte);
				bytesToRead = serialPort1.BytesToRead;
			}
		}

		private void btnFoolsMate_Click(object sender, EventArgs e)
		{
			UARTCommands.AddRange(ChessInterface.move("F2", "F3", solenoid, board));
			UARTCommands.AddRange(ChessInterface.move("E7", "E6", solenoid, board));
			UARTCommands.AddRange(ChessInterface.move("G2", "G4", solenoid, board));
			UARTCommands.AddRange(ChessInterface.move("D8", "H4", solenoid, board));
		}

		private void btnEliminate_Click(object sender, EventArgs e)
		{
			UARTCommands.AddRange(ChessInterface.move("H4", "E1", solenoid, board));
		}
	}
}
