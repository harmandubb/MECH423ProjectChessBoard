using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ChessboardMovement
{
	class ChessInterface
	{

		public static void parseMove(string origin, string destination)
		{
			Tuple<int, int> originCoordinate = new Tuple<int, int>(Convert.ToInt32((char) origin[0]), Convert.ToInt32((char)origin[1]));
			Tuple<int, int> destinationCoordinate = new Tuple<int, int>(Convert.ToInt32((char) destination[0]), Convert.ToInt32((char)destination[1]));

			List<Tuple<int, int>> chessMove = new List<Tuple<int, int>>();

			chessMove.Add(originCoordinate);
			chessMove.Add(destinationCoordinate);
		}
	}

	class Board
	{
		public static int ROWCOLSIZE = 8;
		private int[,] currentBoard = new int [ROWCOLSIZE, ROWCOLSIZE];
		
		public Board()
		{ 
			Array.Clear(this.currentBoard,0,currentBoard.Length);


			//setting white pieces
			for(int row = 0; row < 2; row++)
			{
				for(int col = 0; col < ROWCOLSIZE; col++)
				{
					currentBoard[row, col] = 1;
				}
			}

			//setting black pieces 
			for(int row = 6; row < ROWCOLSIZE; row++)
			{
				for(int col = 0; col < ROWCOLSIZE; col++)
				{
					currentBoard[row, col] = 1;
				}
			}

		}
	}
}
