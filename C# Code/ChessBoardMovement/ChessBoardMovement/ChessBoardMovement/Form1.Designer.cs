
namespace ChessBoardMovement
{
	partial class Form1
	{
		/// <summary>
		///  Required designer variable.
		/// </summary>
		private System.ComponentModel.IContainer components = null;

		/// <summary>
		///  Clean up any resources being used.
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
		///  Required method for Designer support - do not modify
		///  the contents of this method with the code editor.
		/// </summary>
		private void InitializeComponent()
		{
			this.label1 = new System.Windows.Forms.Label();
			this.label2 = new System.Windows.Forms.Label();
			this.txtOrigin = new System.Windows.Forms.TextBox();
			this.txtDestination = new System.Windows.Forms.TextBox();
			this.txtMove = new System.Windows.Forms.TextBox();
			this.label3 = new System.Windows.Forms.Label();
			this.btnSubmit = new System.Windows.Forms.Button();
			this.SuspendLayout();
			// 
			// label1
			// 
			this.label1.AutoSize = true;
			this.label1.Location = new System.Drawing.Point(12, 51);
			this.label1.Name = "label1";
			this.label1.Size = new System.Drawing.Size(40, 15);
			this.label1.TabIndex = 0;
			this.label1.Text = "Origin";
			
			// 
			// label2
			// 
			this.label2.AutoSize = true;
			this.label2.Location = new System.Drawing.Point(135, 51);
			this.label2.Name = "label2";
			this.label2.Size = new System.Drawing.Size(67, 15);
			this.label2.TabIndex = 1;
			this.label2.Text = "Destination";
			// 
			// txtOrigin
			// 
			this.txtOrigin.Location = new System.Drawing.Point(12, 69);
			this.txtOrigin.Name = "txtOrigin";
			this.txtOrigin.Size = new System.Drawing.Size(100, 23);
			this.txtOrigin.TabIndex = 2;
		
			// 
			// txtDestination
			// 
			this.txtDestination.Location = new System.Drawing.Point(135, 69);
			this.txtDestination.Name = "txtDestination";
			this.txtDestination.Size = new System.Drawing.Size(100, 23);
			this.txtDestination.TabIndex = 3;
			// 
			// txtMove
			// 
			this.txtMove.Location = new System.Drawing.Point(12, 127);
			this.txtMove.Name = "txtMove";
			this.txtMove.Size = new System.Drawing.Size(100, 23);
			this.txtMove.TabIndex = 4;
			// 
			// label3
			// 
			this.label3.AutoSize = true;
			this.label3.Location = new System.Drawing.Point(12, 109);
			this.label3.Name = "label3";
			this.label3.Size = new System.Drawing.Size(86, 15);
			this.label3.TabIndex = 5;
			this.label3.Text = "Player to move";
			// 
			// btnSubmit
			// 
			this.btnSubmit.Location = new System.Drawing.Point(254, 69);
			this.btnSubmit.Name = "btnSubmit";
			this.btnSubmit.Size = new System.Drawing.Size(75, 23);
			this.btnSubmit.TabIndex = 6;
			this.btnSubmit.Text = "Submit";
			this.btnSubmit.UseVisualStyleBackColor = true;
			this.btnSubmit.Click += new System.EventHandler(this.btnSubmit_Click);
			// 
			// Form1
			// 
			this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
			this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			this.ClientSize = new System.Drawing.Size(347, 164);
			this.Controls.Add(this.btnSubmit);
			this.Controls.Add(this.label3);
			this.Controls.Add(this.txtMove);
			this.Controls.Add(this.txtDestination);
			this.Controls.Add(this.txtOrigin);
			this.Controls.Add(this.label2);
			this.Controls.Add(this.label1);
			this.Name = "Form1";
			this.Text = "Form1";
			this.ResumeLayout(false);
			this.PerformLayout();

		}

		#endregion

		private System.Windows.Forms.Label label1;
		private System.Windows.Forms.Label label2;
		private System.Windows.Forms.TextBox txtOrigin;
		private System.Windows.Forms.TextBox txtDestination;
		private System.Windows.Forms.TextBox txtMove;
		private System.Windows.Forms.Label label3;
		private System.Windows.Forms.Button btnSubmit;
	}
}

