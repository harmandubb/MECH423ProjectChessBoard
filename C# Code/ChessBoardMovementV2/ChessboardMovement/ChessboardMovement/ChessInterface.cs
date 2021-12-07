using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ChessboardMovement
{
	
	class ChessInterface
	{

		enum directions
		{
			UP = 48,
			RIGHT = 49,
			DOWN = 50,
			LEFT = 51
		}

		byte aAsciValue = 96;

		public static List<Tuple<int,int>> parseMove(string origin, string destination)
		{
			Tuple<int, int> originCoordinate = new Tuple<int, int>(Convert.ToInt32((char) origin[0]), Convert.ToInt32((char)origin[1]));
			Tuple<int, int> destinationCoordinate = new Tuple<int, int>(Convert.ToInt32((char) destination[0]), Convert.ToInt32((char)destination[1]));

			List<Tuple<int, int>> chessCoordinates = new List<Tuple<int, int>>();

			chessCoordinates.Add(originCoordinate);
			chessCoordinates.Add(destinationCoordinate);

			return chessCoordinates;
		}

		public static void move(string origin, string destination)
		{
			List<byte[]> UARTCommands = new List<byte[]>();
			List<Tuple<int, int>> moveCoordinates = new List<Tuple<int, int>>();

			moveCoordinates = parseMove(origin, destination);

			Tuple<int, int> relativeCoordinates = getRelativeCoordinates(moveCoordinates);

			bool solenoidOn = true;

			UARTCommands.Add(moveToNECorner(solenoidOn));


			





		}

		public static Tuple<int, int> getRelativeCoordinates(List<Tuple<int, int>> moveCoordinates)
		{
			Tuple<int, int> relativeCoordinates = new Tuple<int, int>(moveCoordinates[1].Item1 - moveCoordinates[0].Item1, moveCoordinates[1].Item2 - moveCoordinates[0].Item2);

			return relativeCoordinates;
		}

		public static byte[] moveToNECorner(bool solenoidOn)
		{
			byte aAsciValue = 96;
			byte[] buffer = new byte[] { aAsciValue, Convert.ToByte(directions.UP), Convert.ToByte(solenoidOn), aAsciValue, Convert.ToByte(directions.RIGHT), Convert.ToByte(solenoidOn) };

			return buffer;
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

		public bool piecePresent(Tuple<int,int> destination)
		{
			if(this.currentBoard[destination.Item1,destination.Item2] == 1)
			{
				return true;
			} else
			{
				return false; 
			}
			
		}
	}

	class Solenoid

	{

	}
}
