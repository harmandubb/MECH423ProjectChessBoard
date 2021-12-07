using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using 

namespace AutonomousChessBoard
{
	int NUMCOLROWSPACES = 8;
	Tuple<int, int> solenoidLocation = new Tuple<int, int>(0, 0);
	class ChessInterfacing
	{

		public static List<Tuple<int,int>> parseLongAlgebraicNotation(string origin, string destination)
		{
			int originCol, originRow, destinationCol, destinationRow;
			List<Tuple<int, int>> pieceMovementCoordinate = new List<Tuple<int, int>>();

			//Know that the inputs will be a col letter and a row number 

			originCol = Convert.ToInt32((char) origin[0]) - Convert.ToInt32((char)'A');
			originRow = Convert.ToInt32((char) origin[1]) - 1;

			destinationCol = Convert.ToInt32(destination[0]) - Convert.ToInt32((char)'A');
			destinationRow = Convert.ToInt32(destination[1]) - 1;

			Tuple<int, int> originCoordinate = new Tuple<int, int>(originCol,originRow);
			Tuple<int, int> destinationCoordinate = new Tuple<int, int>(destinationCol, destinationRow);

			pieceMovementCoordinate.Add(originCoordinate);
			pieceMovementCoordinate.Add(destinationCoordinate);

			return pieceMovementCoordinate;

		}


	}

	class Board
	{
		public static void setUpBoard()
		{
			//for now a piece will be defined as a 1 
			int[,] board = new int[NUMCOLROWSPACES, NUMCOLROWSPACES];

			Array.Clear(board); //setting all values to zero 

			//set the white pieces on the board
			for(int row = 0; row < 2; row++)
			{
				for (int col = 0; col < NUMCOLROWSPACES; col++)
				{
					board[row, col] = 1;
				}
			}

			//setting the black pieces on the board 
			for (int row = 6; row < NUMCOLROWSPACES; row++)
			{
				for (int col = 0; col < NUMCOLROWSPACES; col++)
				{
					board[row, col] = 1;
				}
			}

		}

		static void destinationPiecePresent(Tuple<int,int> destination)
		{
			bool result = false; 

			if (board[destination.Item1, destination.Item2] == 1)
			{
				result = true;
			}
		}
	}

	class SolenoidMovement
	{

		enum Direction
		{ 
			UP = 48,
			DOWN = 49,
			RIGHT = 50,
			LEFT = 51
		}
		public static Tuple<int,int> getRelativeCoordinates(Tuple<int,int> origin, Tuple<int,int> goTo)
		{
			Tuple<int, int> relativeCoordinates = new Tuple<int, int>(goTo.Item1 - origin.Item1, goTo.Item2 - origin.Item2)
		}

		public static void moveToRightCorner(bool solenoidOn)
		{
			byte[] rightCorner = new byte[] { 97, Direction.UP, solenoidOn, 97, Direction.RIGHT};
		}
	}

}
