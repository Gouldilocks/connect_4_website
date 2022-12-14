import axios from 'axios';
import { apiEndpoint } from './apiConfig';

export async function getMove(board, player) {
  var move = -1;
    await axios.post(`${apiEndpoint}/getMove`, {
      setTimeout: 8000,
      data: {
        board: board,
        player: player
      },
      headers: {
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Origin": "http://ec2-18-208-183-26.compute-1.amazonaws.com:8080",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
      },
      crossDomain: true
    }).then((response) => {
      move = response.data.body
    })
    return move
}