import { useState, useEffect } from 'react';
import Grid2 from '@mui/material/Unstable_Grid2/Grid2';
import empty from '../../assets/BoardImages/empty.png';
import yellow from '../../assets/BoardImages/yellow.png';
import red from '../../assets/BoardImages/red.png';
import nothing from '../../assets/BoardImages/space.png';
import { getMove } from '../../api/MoveApi';

export default function ConnectBoard() {
  const [board, setBoard] = useState([]);
  const [player, setPlayer] = useState(1);
  const colNums = [0, 1, 2, 3, 4, 5, 6];
  const [userCanPlay, setUserCanPlay] = useState(true);
  const [winner, setWinner] = useState(false);

  // Set up the board at the beginning of the game
  useEffect(() => {
    resetBoard();
  }, []);

  // Function to reset the board to all 0
  function resetBoard() {
    const newBoard = [];
    for (let i = 0; i < 6; i++) {
      newBoard.push([]);
      for (let j = 0; j < 7; j++) {
        newBoard[i].push(0);
      }
    }
    setBoard(newBoard);
  }

  // function which will play the AI's turn. It does not allow the user to play while the AI is going
  function runAITurn() {
    setUserCanPlay(false);
    getMove(board, player).then((res) => {
      console.log("got response from getMove")
      console.log(res);
      insertPieceAtCol(res.got, -player, false);
      setUserCanPlay(true);
    });
  }

  function insertPieceAtCol(col, player, runAI) {
    // if there is a winner, we don't want to let anyone play
    if (winner === true) {
      return;
    }
    // if the AI is thinking, don't let the user play
    if (runAI === true && userCanPlay === false) {
      return;
    }
    var newBoard = [...board];
    // Check if the column has an open space
    if (newBoard[0][col] === 0) {
      for (let i = 0; i < 6; i++) {
        if (newBoard[i][col] !== 0) {
          newBoard[i - 1][col] = player;
          break;
        }
        else if (i === 5) {
          newBoard[i][col] = player;
          break;
        }
      }
    }
    else {
      // If the column is full, do nothing
      return;
    }
    setBoard(newBoard);

    if (runAI) {
      runAITurn();
    }

    // Check if the game is over
    if (checkWin(newBoard, player)) {
      setWinner(true);
    }
  }

  // visualize a connect 4 board
  return (
    <>

      
      <Grid2 container spacing={2}
      direction={"row"}
      >
        {/* This is the board itself */}
        <Grid2 item xs={8}>
          <Grid2 container spacing={0}
          direction="row"
          >
            {board.map((row, i) => (
              <Grid2 item xs={12}>
                <Grid2 container spacing={0}
                  direction={"row"}
                >
                    {row.map((col, i) => (
                      <Grid2 item xs={1.25}
                        onClick={() => insertPieceAtCol(i, player, true)}
                      >
                        {
                          (col === 0) ? <img src={empty} alt="empty piece"></img> : (col === -1) ? <img src={yellow} alt="yellow piece"></img> : <img src={red} alt="red piece"></img>
                        }
                      </Grid2>
                    ))}
                  </Grid2>
              </Grid2>
            ))}

          </Grid2>

          <Grid2 container spacing={0}
            direction={"row"}
          >
            {colNums.map((x) => (
              <Grid2 item xs={1.25} onClick={() => { insertPieceAtCol(x, player, true) }}>
                <img src={nothing} alt="empty piece"></img>
              </Grid2>
            ))}
          </Grid2>
        </Grid2>
        {/* End Board itself */}


        {/* This is the options on the right */}
        <Grid2 item xs={2}>
          {!userCanPlay && <h1>AI is thinking...</h1>}
        </Grid2>
        {/* End options on the right */}
      </Grid2>
    </>
  );

}