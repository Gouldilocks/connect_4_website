import { useState, useEffect } from 'react';
import Grid2 from '@mui/material/Unstable_Grid2/Grid2';
import empty from '../../assets/BoardImages/empty.png';
import yellow from '../../assets/BoardImages/yellow.png';
import red from '../../assets/BoardImages/red.png';
import nothing from '../../assets/BoardImages/space.png';
import { getMove, getTerminal, getUtility } from '../../api/MoveApi';
import { Button, Box, ImageList, ImageListItem } from '@mui/material';

export default function ConnectBoard() {
  const [board, setBoard] = useState([]);
  const [player, setPlayer] = useState(1);
  const colNums = [0, 1, 2, 3, 4, 5, 6];
  const [userCanPlay, setUserCanPlay] = useState(true);
  const [winner, setWinner] = useState(false);
  const [theWinner, setTheWinner] = useState(0);
  const [newGame, setNewGame] = useState(true);

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
    setWinner(false);
    setTheWinner(0);
    setUserCanPlay(true);
    setNewGame(true)
    setPlayer(1);
  }

  // function which will play the AI's turn. It does not allow the user to play while the AI is going
  function runAITurn(aiPlayer) {
    setUserCanPlay(false);
    console.log("ai is playing as player: ", -player)
    getMove(board, aiPlayer).then((res) => {
      console.log("got response from getMove")
      console.log(res);
      insertPieceAtCol(res.got, aiPlayer, false);
      setUserCanPlay(true);
    });
  }

  function insertPieceAtCol(col, player, runAI) {
    setNewGame(false);
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
      runAITurn(-player);
    }

    // Check if the game is over
    if (checkTerminal(newBoard, player, runAI)) {
      setWinner(true);
    }
  }

  function findWinner(board, player) {
    getUtility(board, player).then((res) => {
      console.log("got response from getUtility")
      console.log(res);
      if (res.got === "win" && player === 1) {
        alert("Red Wins!");
        setTheWinner(1);
      }
      else if (res.got === "loss" && player === 1) {
        alert("Yellow Wins!");
        setTheWinner(-1);
      }
      else if (res.got === "win" && player === -1) {
        alert("Yellow Wins!");
        setTheWinner(-1);
      }
      else if (res.got === "loss" && player === -1) {
        setTheWinner(1);
        alert("Red Wins!");
      }
      else if (res.got === "draw") {
        alert("Tie!");
        setTheWinner(0);
      }
    });
  }

  function checkTerminal(board, player, AIturn) {
    // Check if the game is over
    if (!AIturn) {
      setUserCanPlay(false);
    }
    getTerminal(board, player).then((res) => {
      console.log("got response from getTerminal")
      console.log(res);
      if (res.got === "true") {
        setWinner(true);
        findWinner(board, player);
        return true;
      }
      else if (res.got === "false") {
        if (!AIturn) {
          setUserCanPlay(true);
        }
        return false;
      }
    });
  }

  function getWinnerAsString(winner) {
    if (winner === 1) {
      return "Red";
    }
    else if (winner === -1) {
      return "Yellow";
    }
    else {
      return "Tie";
    }
  }

  // visualize a connect 4 board
  return (
    <>
      <Grid2 container spacing={0}
      direction={"row"}
        // justifyContent="center"
        // alignItems="center"
      >
        {/* This is the options on the left */}
        <Grid2 item xs={12} md={3}>
          <div>
            To play, just click on one of the columns to drop your first piece! By default, you are player Red, which puts the AI at a disadvantage, but you can change that by clicking the button labeled "PLAY AS YELLOW", and the AI will make the first move. Click "RESET" to reset the board and make the AI play as Yellow again.
          </div>
          <br></br>
          {!userCanPlay && <h1>AI is thinking...</h1>}
          <Button onClick={() => {
            resetBoard();
          }}>Reset</Button>
          {winner && <h1>Winner: {getWinnerAsString(theWinner)}</h1>}
          {newGame && <h1>Start a new game!</h1>}
          {newGame && <Button onClick={() => {
            setPlayer(-1);
            setNewGame(false);
            runAITurn(1);
          }} >Play as Yellow</Button>}
        </Grid2>
        {/* End options on the right */}

        {/* This is the board itself */}
          <ImageList cols={7}>
            {board.map((row, i) => (
              row.map((col, i) => (
                <ImageListItem key={i}
                onClick={() => insertPieceAtCol(i, player, true)}
                >
                <img src={col === 0 ? empty : col === -1 ? yellow : red} />
              </ImageListItem>
              ))
            ))}
          </ImageList>
        </Grid2> 
        {/* End Board itself */}
    </>
  );

}