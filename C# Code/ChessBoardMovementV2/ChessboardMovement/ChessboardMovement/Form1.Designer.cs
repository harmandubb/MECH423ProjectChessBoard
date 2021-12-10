
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
			this.SuspendLayout();
			// 
			// serialPort1
			// 
			this.serialPort1.PortName = "COM4";
			// 
			// label1
			// 
			this.label1.AutoSize = true;
			this.label1.Location = new System.Drawing.Point(9, 45);
			this.label1.Name = "label1";
			this.label1.Size = new System.Drawing.Size(34, 13);
			this.label1.TabIndex = 0;
			this.label1.Text = "Origin";
			// 
			// txtDestination
			// 
			this.txtDestination.Location = new System.Drawing.Point(127, 61);
			this.txtDestination.Name = "txtDestination";
			this.txtDestination.Size = new System.Drawing.Size(100, 20);
			this.txtDestination.TabIndex = 1;
			// 
			// btnSubmit
			// 
			this.btnSubmit.Location = new System.Drawing.Point(233, 58);
			this.btnSubmit.Name = "btnSubmit";
			this.btnSubmit.Size = new System.Drawing.Size(75, 23);
			this.btnSubmit.TabIndex = 2;
			this.btnSubmit.Text = "Submit";
			this.btnSubmit.UseVisualStyleBackColor = true;
			this.btnSubmit.Click += new System.EventHandler(this.btnSubmit_Click);
			// 
			// txtOrigin
			// 
			this.txtOrigin.Location = new System.Drawing.Point(12, 61);
			this.txtOrigin.Name = "txtOrigin";
			this.txtOrigin.Size = new System.Drawing.Size(100, 20);
			this.txtOrigin.TabIndex = 3;
			// 
			// none
			// 
			this.none.AutoSize = true;
			this.none.Location = new System.Drawing.Point(124, 45);
			this.none.Name = "none";
			this.none.Size = new System.Drawing.Size(60, 13);
			this.none.TabIndex = 4;
			this.none.Text = "Destination";
			// 
			// txtMove
			// 
			this.txtMove.Location = new System.Drawing.Point(12, 103);
			this.txtMove.Name = "txtMove";
			this.txtMove.Size = new System.Drawing.Size(100, 20);
			this.txtMove.TabIndex = 6;
			// 
			// label3
			// 
			this.label3.AutoSize = true;
			this.label3.Location = new System.Drawing.Point(9, 87);
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
			// Form1
			// 
			this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
			this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			this.ClientSize = new System.Drawing.Size(800, 450);
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
	}
}

