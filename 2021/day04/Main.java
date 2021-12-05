import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.Vector;
import java.util.Arrays;

public class Main {
  public static void main(String[] args) {
    var lines = readFile("data-input");
    var data = parseInput(lines);

    int result = 0;

    // PART1
    // for (int i = 0; i < data.draws.length; i++) {
    //   boolean hasWon = false;
    //   var mark = data.draws[i];
    //   for (int j = 0; j < data.boards.size(); j++) {
    //     var currBoard = data.boards.elementAt(j);
    //     currBoard.mark(mark);
    //     if (currBoard.isBingo()) {
    //       System.out.println("A board won with: " + mark);
    //       var score = currBoard.score();
    //       result = score * Integer.parseInt(mark);
    //       hasWon = true;
    //       break;
    //     }
    //   }

    //   if (hasWon) {
    //     break;
    //   }
    // }

    for (int i = 0; i < data.draws.length; i++) {
      boolean hasWon = false;
      var mark = data.draws[i];
      for (int j = 0; j < data.boards.size(); j++) {
        var currBoard = data.boards.elementAt(j);
        currBoard.mark(mark);
        if (currBoard.isBingo()) {
          System.out.println("A board won with: " + mark);

          if (data.boards.size() > 1) {
            System.out.println("Remove board at index" + j);
            data.boards.remove(j);
            // redo this number again
            j--;
          } else {
            System.out.println("Last board remaining so calculating score");
            var score = currBoard.score();
            result = score * Integer.parseInt(mark);
            hasWon = true;
            break;
          }
        }
      }

      if (hasWon) {
        break;
      }
    }

    System.out.println("Result: " + result);
  }

  private static Vector<String> readFile(String filename) {
    Vector<String> lines = new Vector<String>();
    try {
      File file = new File(filename);
      Scanner scanner = new Scanner(file);
      while (scanner.hasNextLine()) {
        String data = scanner.nextLine();
        lines.add(data);
      }
      scanner.close();
    } catch (FileNotFoundException e) {
      return lines;
    }

    return lines;
  }

  private static Data parseInput(Vector<String> input) {
    String[] draws = input.elementAt(0).split(",", 0);
    Vector<Board> boards = new Vector<Board>();

    // initialized but not used
    Board currBoard = new Board();
    for (int i = 2; i < input.size(); i++) {
      if ("".equals(input.elementAt(i))) {
        currBoard = new Board();
        continue;
      }

      String[] row = input.elementAt(i).split(" ");
      row = Arrays.stream(row).filter(r -> !"".equals(r)).toArray(String[]::new);
      currBoard.add(row);

      if (currBoard.size() == 5) {
        boards.add(currBoard);
      }
    }

    return new Data(draws, boards);
  }
}

class Board {
  String[][] board;
  Boolean[][] seen;
  int size = 0;

  public Board() {
    board = new String[5][];

    // I know it's a 5x5 board and my java skills are lacking so i'm blehh now
    seen = new Boolean[5][5];
    for (Boolean[] row: seen) {
      Arrays.fill(row, false);
    }
  }

  public void add(String[] entry) {
    if (size == 5) {
      System.err.println("why you go over limit 5");
      System.exit(1);
    }
    board[size] = entry;
    size++;
  }

  public int size() {
    return size;
  }

  public void mark(String tick) {
    for (int row = 0; row < board.length; row++) {
      for (int col = 0; col < board[row].length; col++) {
        if (tick.equals(board[row][col])) {
          seen[row][col] = true;
        }
      }
    }
  }

  public boolean isBingo() {
    for (int row = 0; row < seen.length; row++) {
      int rowCount = 0;
      int colCount = 0;
      for (int col = 0; col < seen[row].length; col++) {
        if (seen[row][col]) {
          rowCount++;
        }

        if (seen[col][row]) {
          colCount++;
        }
      }

      if (rowCount == 5 || colCount ==  5) {
        return true;
      }
    }

    return false;
  }

  public int score() {
    int sum = 0;
    for (int row = 0; row < seen.length; row++) {
      String rowOutput = "";
      for (int col = 0; col < seen[row].length; col++) {
        if (!seen[row][col]) {
          sum += Integer.parseInt(board[row][col]);
          // System.out.println(sum);
        }

        String n = board[row][col];
        if (Integer.parseInt(board[row][col]) < 10) {
          n = " " + n;
        }
        if (seen[row][col]) {
          rowOutput += n + "* ";
        } else {
          rowOutput += n + "^ ";
        }
      }

      System.out.println(rowOutput);
    }

    return sum;
  }
}

class Data {
  String[] draws;
  Vector<Board> boards;

  public Data(String[] inputDraws, Vector<Board> inputBoards) {
    draws = inputDraws;
    boards = inputBoards;
  }
}