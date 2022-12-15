import React from "react";
import ConnectBoard from "../components/ConnectBoard/ConnectBoard";

export default function Mainpage() {
  return (
    <>
      <h1>Hello! Welcome to my Connect 4 AI Webpage!</h1>
      <p> My name is Christian Gould, and I developed this AI Fall 2022 to
        play connect 4 while taking the course
        CS-5320, and entered the competition for the best AI.
      </p>
      <p>
        I am a student at Southern Methodist University, and I will be graduating
        in May 2023. I am currently a senior, majoring in Computer Science.
      </p>
      <p>
        This AI won the competition, and I am very proud of it. I hope you enjoy.
        If you would like to know more about how the AI works, check out the description below the board.
      </p>
      <a href="https://cgould.net">Check out my personal website!</a>
      <p></p>
      <ConnectBoard />
      <h3>
        How the AI Works:
      </h3>
      <p>
        The AI uses a minimax algorithm with alpha-beta pruning to determine the best move at any point in time.
      </p>
      <p>
        When this AI was playing against other AI's the depth that it searched was deeper than this webpage, but I made it so that it only searches 7 moves deep here, so that it doesn't take too long to load. Even so, a human being would have an extremely hard time beating this AI. I created it, and played against it tons of times, and I have never won haha.
      </p>
      <h4>
        The Evaluation Function
      </h4>
      <p>
        The interesting thing about creating an AI that plays using the minimax algorithm is that you have to create an evaluation function that determines how good a board is for the AI, and it also uses that same evaluation to determine how good its opponent's possible moves are.
      </p>
      <p>
        The evaluation function that I chose to use is simple, so that it could more properly evaluate positions quickly. In the beginning stages of the game, it aims to get itself the zugzwang. The zugzwang is a property where the person who controlls the zugzwang has the advantage, where the opponent's every move moves against them. Yellow is able to control the zugzwang if it has 3 yellow pieces in a row, and the 4th piece that it needs is on an even row. Even rows start with the second from the bottom, and is every other row. The same can be said for red, but they are on odd rows starting with the first row. If nobody has a win on their respective row, then mathematically red has the zugzwang. This is because red has the first move, and therefore has a distinct advantage.
      </p>
      <p>
        The way my AI approaches the zugzwang is that it will try to get the zugzwang, and then will try to block all the possible wins that the opponent has. This forces the opponent to play into the AI's win that it set up in the earlier portions of the game. This is the main way that the AI wins, and it is very effective.
      </p>
    </>
  );
}