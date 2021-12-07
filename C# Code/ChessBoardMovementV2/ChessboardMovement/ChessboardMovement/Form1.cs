﻿using System;
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
		public Form1()
		{
			InitializeComponent();
			Board board = new Board();
		}

		private void btnSubmit_Click(object sender, EventArgs e)
		{
			string origin = txtOrigin.Text;
			string destination = txtDestination.Text;

			ChessInterface.parseMove(origin, destination);
		}
	}
}
