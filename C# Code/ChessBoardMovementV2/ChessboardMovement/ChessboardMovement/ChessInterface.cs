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
			UP = 51,
			RIGHT = 48,
			DOWN = 49,
			LEFT = 50
		}

		byte aAsciValue = 97;

		public static List<Tuple<int,int>> parseMove(string origin, string destination)
		{
			Tuple<int, int> originCoordinate = new Tuple<int, int>(Convert.ToInt32(origin[1])-48 - 1, Convert.ToInt32((char)origin[0]) - 65);
			Tuple<int, int> destinationCoordinate = new Tuple<int, int>(Convert.ToInt32(destination[1])-48- 1, Convert.ToInt32((char)destination[0]) - 65);

			List<Tuple<int, int>> chessCoordinates = new List<Tuple<int, int>>();

			chessCoordinates.Add(originCoordinate);
			chessCoordinates.Add(destinationCoordinate);

			return chessCoordinates;
		}

		public static List<byte[]> move(string origin, string destination, Solenoid solenoid, Board board)
		{
			List<byte[]> UARTCommands = new List<byte[]>();
			List<Tuple<int, int>> playerMove = new List<Tuple<int, int>>();
			List<byte[]> temp = new List<byte[]>();
			bool solenoidOn;

			playerMove = parseMove(origin, destination);

			

			//determine if a piece needs to be moved out of the way
			if (board.piecePresent(playerMove[1]))
			{
				solenoidOn = false;
				//move the piece out of the way by moving the solenoid from it's current position to be under the piece to move
				Tuple<int, int> goToElimatePieceRelativeCoordinate = getRelativeCoordinates(solenoid.getLocation(), playerMove[1]);
				UARTCommands.AddRange(moveToNECorner(solenoidOn));
				UARTCommands.AddRange(moveToDestination(solenoidOn, goToElimatePieceRelativeCoordinate));
				UARTCommands.AddRange(moveToCenter(solenoidOn));

				solenoid.setLocation(playerMove[1]);

				//eliminate the piece
				solenoidOn = true;
				UARTCommands.AddRange(moveToNECorner(solenoidOn));
				UARTCommands.AddRange(moveToTheEdgeOfBoard(solenoidOn, playerMove[1]));
				UARTCommands.AddRange(moveHalfToLeft(solenoidOn));

				////can drop the piece 
				solenoidOn = false;
				UARTCommands.AddRange(moveHalfToRight(solenoidOn));
				UARTCommands.AddRange(moveHalfToRight(solenoidOn));
				UARTCommands.AddRange(moveHalfToRight(solenoidOn));
				UARTCommands.AddRange(moveToCenter(solenoidOn));

				//updating the solenoid location
				solenoid.setLocation(Tuple.Create(playerMove[1].Item1, 0 ));
			}

			//need to move solenoid to origin location 

			solenoidOn = false;

			//Tuple<int, int> goToOriginRelativeCoordinate = getRelativeCoordinates(solenoid.getLocation(), playerMove[0]);
			//UARTCommands.AddRange(moveToNECorner(solenoidOn));
			//UARTCommands.AddRange(moveToDestination(solenoidOn, goToOriginRelativeCoordinate));
			//UARTCommands.AddRange(moveToCenter(solenoidOn));

			//solenoid.setLocation(playerMove[0]);


			////////conduct the players move 
			//solenoidOn = true;
			//Tuple<int, int> relativePlayerMoveCoordinates = getRelativeCoordinates(playerMove[0], playerMove[1]);

			//UARTCommands.AddRange(moveToNECorner(solenoidOn));
			//UARTCommands.AddRange(moveToDestination(solenoidOn, relativePlayerMoveCoordinates));
			//UARTCommands.AddRange(moveToCenter(solenoidOn));

			//solenoid.setLocation(playerMove[0]);

			//solenoidOn = false;

			return UARTCommands;
		}

		public static Tuple<int, int> getRelativeCoordinates(Tuple<int, int> origin, Tuple<int,int> destination)
		{
			Tuple<int, int> relativeCoordinates = new Tuple<int, int>(destination.Item2 - origin.Item2, destination.Item1 - origin.Item1);

			return relativeCoordinates;
		}

		public static List<byte[]> moveToNECorner(bool solenoidOn)
		{
			byte aAsciValue = 97;

			List<byte[]> commands = new List<byte[]>
			{
				new byte[] {aAsciValue, Convert.ToByte(directions.UP), Convert.ToByte(solenoidOn) },
				new byte[] {aAsciValue, Convert.ToByte(directions.RIGHT), Convert.ToByte(solenoidOn)}
			};

			return commands;
		}

		public static List<byte[]> moveToCenter(bool solenoidOn)
		{
			byte aAsciValue = 97;

			List<byte[]> commands = new List<byte[]>
			{
				new byte[] {aAsciValue, Convert.ToByte(directions.DOWN), Convert.ToByte(solenoidOn)},
				new byte[] {aAsciValue, Convert.ToByte(directions.LEFT), Convert.ToByte(solenoidOn)}
			};

			return commands;
		}

		public static List<byte[]> moveHalfToLeft(bool solenoidOn)
		{
			byte aAsciValue = 97;

			List<byte[]> commands = new List<byte[]>
			{
				new byte[] {aAsciValue, Convert.ToByte(directions.LEFT), Convert.ToByte(solenoidOn)}
			};

			return commands;
		}

		public static List<byte[]> moveHalfToRight(bool solenoidOn)
		{
			byte aAsciValue = 97;

			List<byte[]> commands = new List<byte[]>
			{
				new byte[] {aAsciValue, Convert.ToByte(directions.RIGHT), Convert.ToByte(solenoidOn)}
			};

			return commands;
		}

		public static List<byte[]> moveToTheEdgeOfBoard(bool solenoidOn, Tuple<int,int> currentCoordinates)
		{
			byte aAsciValue = 97;
			List<byte[]> movement = new List<byte[]>();
			int LEFTRIGHT = 0;
			byte[] temp = new byte[3];

			//if (currentCoordinates.Item2 >= 5)
			//{
			//	LEFTRIGHT = (int)directions.RIGHT;
			//}
			//else
			//{
			//	LEFTRIGHT = (int)directions.LEFT;
			//}

			LEFTRIGHT = (int)directions.LEFT;

			//bias moving to the left for now and make the game smarter afterwards 
			for (int i = 0; i < currentCoordinates.Item2 + 1; i++)
			{
				for (int j = 0; j < 2; j++)
				{
					temp = new byte[] { aAsciValue, Convert.ToByte(LEFTRIGHT), Convert.ToByte(solenoidOn) };
					movement.Add(temp);
				}
			}

			return movement;
		}



		public static List<byte[]> moveToDestination(bool solenoidOn, Tuple<int,int> relativeCoordinates)
		{
			byte aAsciValue = 97;

			int UPDOWN = 0;
			int RIGHTLEFT = 0;

			List<byte[]> mainMovements = new List<byte[]>();
			byte[] temp = new byte[3];

			if (relativeCoordinates.Item2 > 0)
			{
				UPDOWN = (int) directions.UP;
			} else
			{
				UPDOWN = (int)directions.DOWN;
			}

			if (relativeCoordinates.Item1 > 0)
			{
				RIGHTLEFT = (int)directions.RIGHT;
			}
			else
			{
				RIGHTLEFT = (int)directions.LEFT;
			}

		
			//move up and down first 
			for(int i = 0;  i < Math.Abs(relativeCoordinates.Item2); i++)
			{
				//need two half steps to move one square 
				for(int j = 0; j < 2; j++)
				{
					temp = new byte[] { aAsciValue, Convert.ToByte(UPDOWN), Convert.ToByte(solenoidOn) };
					mainMovements.Add(temp);
				}
				
			}

			//move right and left 
			for (int i = 0; i < Math.Abs(relativeCoordinates.Item1); i++)
			{
				//need two half steps to move one square 
				for (int j = 0; j < 2; j++)
				{
					temp = new byte[] { aAsciValue, Convert.ToByte(RIGHTLEFT), Convert.ToByte(solenoidOn) };
					mainMovements.Add(temp);
				}

			}

			return mainMovements;
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
		private Tuple<int, int> location;

		public Solenoid()
		{
			this.location = new Tuple<int, int>(0, 0); 
		}

		public void setLocation(Tuple<int,int> newLocation)
		{
			this.location = newLocation;
		}

		public Tuple<int,int> getLocation()
		{
			return this.location;
		}


	}
}
