"use strict";

(() => {
  const EMPTY = "";
  const X = "X";
  const O = "O";
  const CENTER = 4;
  const WINS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6],
  ];
  const boardElement = document.querySelector("#board");
  const cells = [...document.querySelectorAll(".cell")];
  const statusElement = document.querySelector("#status");
  const statusMark = document.querySelector("#status-mark");
  const statusRow = document.querySelector(".status-row");
  const difficulty = document.querySelector("#difficulty");
  const scores = { X: 0, O: 0, draws: 0 };
  let board = Array(9).fill(EMPTY);
  let gameOver = false;
  let aiThinking = false;
  let roundTimer = null;
  let winningLine = [];

  function availableMoves(position = board) {
    return position.flatMap((cell, index) => cell === EMPTY ? [index] : []);
  }

  function result(position) {
    for (const line of WINS) {
      const [a, b, c] = line;
      if (position[a] && position[a] === position[b] && position[a] === position[c]) {
        return { winner: position[a], line };
      }
    }
    return position.every(Boolean) ? { winner: null, line: null, draw: true } : null;
  }

  function terminalScore(state, depth, aiPlayer, humanPlayer) {
    if (!state) return null;
    if (state.winner === aiPlayer) return 10 - depth;
    if (state.winner === humanPlayer) return depth - 10;
    if (state.draw) return 0;
    return null;
  }

  function minimax(position, depth, maximizing, aiPlayer, humanPlayer) {
    const terminal = terminalScore(result(position), depth, aiPlayer, humanPlayer);
    if (terminal !== null) return terminal;
    const player = maximizing ? aiPlayer : humanPlayer;
    let best = maximizing ? -Infinity : Infinity;
    for (const move of availableMoves(position)) {
      position[move] = player;
      const score = minimax(position, depth + 1, !maximizing, aiPlayer, humanPlayer);
      position[move] = EMPTY;
      best = maximizing ? Math.max(best, score) : Math.min(best, score);
    }
    return best;
  }

  function bestMove(position, aiPlayer = O) {
    const moves = availableMoves(position);
    if (!moves.length) return null;
    if (moves.length === 9) return CENTER;
    const humanPlayer = aiPlayer === O ? X : O;
    let bestScore = -Infinity;
    let bestMoves = [];
    for (const move of moves) {
      position[move] = aiPlayer;
      const score = minimax(position, 0, false, aiPlayer, humanPlayer);
      position[move] = EMPTY;
      if (score > bestScore) {
        bestScore = score;
        bestMoves = [move];
      } else if (score === bestScore) {
        bestMoves.push(move);
      }
    }
    if (bestMoves.includes(CENTER)) return CENTER;
    return bestMoves[Math.floor(Math.random() * bestMoves.length)];
  }

  function immediateWin(position, player) {
    for (const move of availableMoves(position)) {
      position[move] = player;
      const wins = result(position)?.winner === player;
      position[move] = EMPTY;
      if (wins) return move;
    }
    return null;
  }

  function aiMove() {
    const moves = availableMoves();
    if (!moves.length) return null;
    if (difficulty.value === "easy") return moves[Math.floor(Math.random() * moves.length)];
    if (difficulty.value === "medium") {
      const win = immediateWin(board, O);
      if (win !== null) return win;
      const block = immediateWin(board, X);
      if (block !== null) return block;
      if (Math.random() >= 0.6) return moves[Math.floor(Math.random() * moves.length)];
    }
    return bestMove(board, O);
  }

  function updateStatus(message, mark = "", tone = "") {
    statusElement.textContent = message;
    statusMark.textContent = mark;
    statusMark.className = `status-mark ${tone}`;
    statusRow.classList.toggle("thinking", aiThinking);
  }

  function render() {
    cells.forEach((cell, index) => {
      const value = board[index];
      cell.textContent = value;
      cell.disabled = gameOver || aiThinking || Boolean(value);
      cell.classList.toggle("x", value === X);
      cell.classList.toggle("o", value === O);
      cell.classList.toggle("win", winningLine.includes(index));
      const row = Math.floor(index / 3) + 1;
      const column = (index % 3) + 1;
      cell.setAttribute("aria-label", `Row ${row}, column ${column}, ${value || "empty"}`);
    });
    document.querySelector("#score-x").textContent = scores.X;
    document.querySelector("#score-o").textContent = scores.O;
    document.querySelector("#score-draw").textContent = scores.draws;
  }

  function finishGame(outcome) {
    gameOver = true;
    aiThinking = false;
    if (outcome.winner) {
      scores[outcome.winner] += 1;
      winningLine = outcome.line;
      if (outcome.winner === X) updateStatus("You win! New round starting…", X, "x-text");
      else updateStatus("AI wins. New round starting…", O, "o-text");
    } else {
      scores.draws += 1;
      updateStatus("It's a draw! New round starting…", "", "");
    }
    render();
    roundTimer = window.setTimeout(resetRound, 1500);
  }

  function place(index, player) {
    board[index] = player;
    const outcome = result(board);
    if (outcome) {
      finishGame(outcome);
      return true;
    }
    return false;
  }

  function onPlayerMove(event) {
    const index = Number(event.currentTarget.dataset.cell);
    if (gameOver || aiThinking || board[index]) return;
    if (place(index, X)) return;
    aiThinking = true;
    updateStatus("AI is thinking…", O, "o-text");
    render();
    window.setTimeout(() => {
      if (gameOver) return;
      const move = aiMove();
      if (move !== null) place(move, O);
      aiThinking = false;
      if (!gameOver) updateStatus("Your turn", X, "x-text");
      render();
    }, 300);
  }

  function resetRound() {
    if (roundTimer !== null) window.clearTimeout(roundTimer);
    roundTimer = null;
    board = Array(9).fill(EMPTY);
    winningLine = [];
    gameOver = false;
    aiThinking = false;
    updateStatus("Your turn", X, "x-text");
    render();
  }

  cells.forEach((cell) => cell.addEventListener("click", onPlayerMove));
  document.querySelector("#restart").addEventListener("click", resetRound);
  document.querySelector("#reset-scores").addEventListener("click", () => {
    scores.X = 0;
    scores.O = 0;
    scores.draws = 0;
    render();
  });
  difficulty.addEventListener("change", resetRound);
  boardElement.addEventListener("keydown", (event) => {
    if (!/^Arrow/.test(event.key)) return;
    const current = document.activeElement;
    const index = Number(current?.dataset?.cell);
    if (!Number.isInteger(index)) return;
    event.preventDefault();
    const delta = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -3, ArrowDown: 3 }[event.key];
    const next = (index + delta + 9) % 9;
    cells[next].focus();
  });

  updateStatus("Your turn", X, "x-text");
  render();
})();
