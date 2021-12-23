
namespace ChessboardMovement
{
	partial class Form1
	{
		/// <summary>
		/// Required designer variable.
		/// </summary>
		private System.ComponentModel.IContainer components = null;

		/// <summary>
		/// Clean up any resources being used.
		/// </summary>
		/// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
		protected override void Dispose(bool disposing)
		{
			if (disposing && (components != null))
			{
				components.Dispose();
			}
			base.Dispose(disposing);
		}

		#region Windows Form Designer generated code

		/// <summary>
		/// Required method for Designer support - do not modify
		/// the contents of this method with the code editor.
		/// </summary>
		private void InitializeComponent()
		{
			this.components = new System.ComponentModel.Container();
			this.serialPort1 = new System.IO.Ports.SerialPort(this.components);
			this.label1 = new System.Windows.Forms.Label();
			this.txtDestination = new System.Windows.Forms.TextBox();
			this.btnSubmit = new System.Windows.Forms.Button();
			this.txtOrigin = new System.Windows.Forms.TextBox();
			this.none = new System.Windows.Forms.Label();
			this.txtMove = new System.Windows.Forms.TextBox();
			this.label3 = new System.Windows.Forms.Label();
			this.timer1 = new System.Windows.Forms.Timer(this.components);
			this.comboBoxCOMPorts = new System.Windows.Forms.ComboBox();
			this.btnConnectDisconnect = new System.Windows.Forms.Button();
			this.txtSerialBytes = new System.Windows.Forms.TextBox();
			this.btnFoolsMate = new System.Windows.Forms.Button();
			this.btnEliminate = new System.Windows.Forms.Button();
			this.Debugging = new System.Windows.Forms.Label();
			this.label2 = new System.Windows.Forms.Label();
			this.label4 = new System.Windows.Forms.Label();
			this.label5 = new System.Windows.Forms.Label();
			this.SuspendLayout();
			// 
			// serialPort1
			// 
			this.serialPort1.PortName = "COM4";
			this.serialPort1.DataReceived += new System.IO.Ports.SerialDataReceivedEventHandler(this.PortDataReceived);
			// 
			// label1
			// 
			this.label1.AutoSize = true;
			this.label1.Location = new System.Drawing.Point(9, 106);
			this.label1.Name = "label1";
			this.label1.Size = new System.Drawing.Size(34, 13);
			this.label1.TabIndex = 0;
			this.label1.Text = "Origin";
			// 
			// txtDestination
			// 
			this.txtDestination.Location = new System.Drawing.Point(127, 122);
			this.txtDestination.Name = "txtDestination";
			this.txtDestination.Size = new System.Drawing.Size(100, 20);
			this.txtDestination.TabIndex = 1;
			// 
			// btnSubmit
			// 
			this.btnSubmit.Location = new System.Drawing.Point(233, 119);
			this.btnSubmit.Name = "btnSubmit";
			this.btnSubmit.Size = new System.Drawing.Size(75, 23);
			this.btnSubmit.TabIndex = 2;
			this.btnSubmit.Text = "Submit";
			this.btnSubmit.UseVisualStyleBackColor = true;
			this.btnSubmit.Click += new System.EventHandler(this.btnSubmit_Click);
			// 
			// txtOrigin
			// 
			this.txtOrigin.Location = new System.Drawing.Point(12, 122);
			this.txtOrigin.Name = "txtOrigin";
			this.txtOrigin.Size = new System.Drawing.Size(100, 20);
			this.txtOrigin.TabIndex = 3;
			// 
			// none
			// 
			this.none.AutoSize = true;
			this.none.Location = new System.Drawing.Point(124, 106);
			this.none.Name = "none";
			this.none.Size = new System.Drawing.Size(60, 13);
			this.none.TabIndex = 4;
			this.none.Text = "Destination";
			// 
			// txtMove
			// 
			this.txtMove.Location = new System.Drawing.Point(325, 121);
			this.txtMove.Name = "txtMove";
			this.txtMove.Size = new System.Drawing.Size(100, 20);
			this.txtMove.TabIndex = 6;
			// 
			// label3
			// 
			this.label3.AutoSize = true;
			this.label3.Location = new System.Drawing.Point(322, 105);
			this.label3.Name = "label3";
			this.label3.Size = new System.Drawing.Size(78, 13);
			this.label3.TabIndex = 5;
			this.label3.Text = "Player to Move";
			// 
			// timer1
			// 
			this.timer1.Enabled = true;
			this.timer1.Interval = 300;
			this.timer1.Tick += new System.EventHandler(this.timer1_Tick);
			// 
			// comboBoxCOMPorts
			// 
			this.comboBoxCOMPorts.FormattingEnabled = true;
			this.comboBoxCOMPorts.Location = new System.Drawing.Point(12, 12);
			this.comboBoxCOMPorts.Name = "comboBoxCOMPorts";
			this.comboBoxCOMPorts.Size = new System.Drawing.Size(121, 21);
			this.comboBoxCOMPorts.TabIndex = 7;
			// 
			// btnConnectDisconnect
			// 
			this.btnConnectDisconnect.Location = new System.Drawing.Point(152, 10);
			this.btnConnectDisconnect.Name = "btnConnectDisconnect";
			this.btnConnectDisconnect.Size = new System.Drawing.Size(75, 23);
			this.btnConnectDisconnect.TabIndex = 8;
			this.btnConnectDisconnect.Text = "Connect Serial";
			this.btnConnectDisconnect.UseVisualStyleBackColor = true;
			this.btnConnectDisconnect.Click += new System.EventHandler(this.btnConnectDisconnect_Click);
			// 
			// txtSerialBytes
			// 
			this.txtSerialBytes.Location = new System.Drawing.Point(12, 169);
			this.txtSerialBytes.Multiline = true;
			this.txtSerialBytes.Name = "txtSerialBytes";
			this.txtSerialBytes.Size = new System.Drawing.Size(215, 114);
			this.txtSerialBytes.TabIndex = 9;
			// 
			// btnFoolsMate
			// 
			this.btnFoolsMate.Location = new System.Drawing.Point(256, 196);
			this.btnFoolsMate.Name = "btnFoolsMate";
			this.btnFoolsMate.Size = new System.Drawing.Size(75, 23);
			this.btnFoolsMate.TabIndex = 10;
			this.btnFoolsMate.Text = "Fools Mate";
			this.btnFoolsMate.UseVisualStyleBackColor = true;
			this.btnFoolsMate.Click += new System.EventHandler(this.btnFoolsMate_Click);
			// 
			// btnEliminate
			// 
			this.btnEliminate.Location = new System.Drawing.Point(256, 237);
			this.btnEliminate.Name = "btnEliminate";
			this.btnEliminate.Size = new System.Drawing.Size(75, 23);
			this.btnEliminate.TabIndex = 11;
			this.btnEliminate.Text = "Eliminate";
			this.btnEliminate.UseVisualStyleBackColor = true;
			this.btnEliminate.Click += new System.EventHandler(this.btnEliminate_Click);
			// 
			// Debugging
			// 
			this.Debugging.AutoSize = true;
			this.Debugging.Location = new System.Drawing.Point(12, 153);
			this.Debugging.Name = "Debugging";
			this.Debugging.Size = new System.Drawing.Size(59, 13);
			this.Debugging.TabIndex = 12;
			this.Debugging.Text = "Debugging";
			// 
			// label2
			// 
			this.label2.AutoSize = true;
			this.label2.Location = new System.Drawing.Point(253, 169);
			this.label2.Name = "label2";
			this.label2.Size = new System.Drawing.Size(94, 13);
			this.label2.TabIndex = 13;
			this.label2.Text = "Pre-loaded Games";
			// 
			// label4
			// 
			this.label4.AutoSize = true;
			this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F);
			this.label4.Location = new System.Drawing.Point(9, 50);
			this.label4.Name = "label4";
			this.label4.Size = new System.Drawing.Size(466, 17);
			this.label4.TabIndex = 14;
			this.label4.Text = "Use long algebraic chess notation for orgin and destination coordinates. ";
			this.label4.Click += new System.EventHandler(this.label4_Click);
			// 
			// label5
			// 
			this.label5.AutoSize = true;
			this.label5.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F);
			this.label5.Location = new System.Drawing.Point(9, 73);
			this.label5.Name = "label5";
			this.label5.Size = new System.Drawing.Size(423, 17);
			this.label5.TabIndex = 15;
			this.label5.Text = "Example: Origin = E2 Destination = E4 will move pawn on E2 to E4";
			// 
			// Form1
			// 
			this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
			this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			this.ClientSize = new System.Drawing.Size(475, 290);
			this.Controls.Add(this.label5);
			this.Controls.Add(this.label4);
			this.Controls.Add(this.label2);
			this.Controls.Add(this.Debugging);
			this.Controls.Add(this.btnEliminate);
			this.Controls.Add(this.btnFoolsMate);
			this.Controls.Add(this.txtSerialBytes);
			this.Controls.Add(this.btnConnectDisconnect);
			this.Controls.Add(this.comboBoxCOMPorts);
			this.Controls.Add(this.txtMove);
			this.Controls.Add(this.label3);
			this.Controls.Add(this.none);
			this.Controls.Add(this.txtOrigin);
			this.Controls.Add(this.btnSubmit);
			this.Controls.Add(this.txtDestination);
			this.Controls.Add(this.label1);
			this.Name = "Form1";
			this.Text = "Form1";
			this.Load += new System.EventHandler(this.Form1_Load);
			this.ResumeLayout(false);
			this.PerformLayout();

		}

		#endregion

		private System.IO.Ports.SerialPort serialPort1;
		private System.Windows.Forms.Label label1;
		private System.Windows.Forms.TextBox txtDestination;
		private System.Windows.Forms.Button btnSubmit;
		private System.Windows.Forms.TextBox txtOrigin;
		private System.Windows.Forms.Label none;
		private System.Windows.Forms.TextBox txtMove;
		private System.Windows.Forms.Label label3;
		private System.Windows.Forms.Timer timer1;
		private System.Windows.Forms.ComboBox comboBoxCOMPorts;
		private System.Windows.Forms.Button btnConnectDisconnect;
		private System.Windows.Forms.TextBox txtSerialBytes;
		private System.Windows.Forms.Button btnFoolsMate;
		private System.Windows.Forms.Button btnEliminate;
		private System.Windows.Forms.Label Debugging;
		private System.Windows.Forms.Label label2;
		private System.Windows.Forms.Label label4;
		private System.Windows.Forms.Label label5;
	}
}

