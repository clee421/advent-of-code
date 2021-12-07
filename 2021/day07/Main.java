import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class Main {
  public static void main(String[] args) {
    var nums = readFile("data-input");
    var result = solve(nums);

    System.out.println("Horizontal: " + result);
  }

  private static long solve(Vector<Integer> horizontal) {
    int min = -1;
    for (int i = 0; i < horizontal.size(); i++) {
      int tempMin = calculateFuel(i, horizontal);
      // System.out.println("position " + tempMin);
      if (min == -1 || tempMin < min) {
        min = tempMin;
      }
    }

    return min;
  }

  private static int calculateFuel(int pos, Vector<Integer> horizontal) {
    int sum = 0;
    for (int i = 0; i < horizontal.size(); i++) {
      int calc = pos - horizontal.elementAt(i);
      if (calc < 0) {
        calc = -calc;
      }

      // part 1
      // sum += calc;

      // part 2
      int f = crabFuel(calc);
      // if (pos == 5) {
      //   System.out.println(horizontal.elementAt(i) + " -> " + pos + " is " + calc + "; fuel " + f);
      // }
      sum += f;
    }

    return sum;
  }

  // sum of integers formula
  private static int crabFuel(int fuel) {
    if (fuel < 2) {
      return fuel;
    }

    int firstTerm = 1;
    int lastTerm = fuel;

    return lastTerm*(firstTerm + lastTerm) / 2;
  }

  private static Vector<Integer> readFile(String filename) {
    Vector<String> lines = new Vector<String>();
    Vector<Integer> nums = new Vector<Integer>();
    try {
      File file = new File(filename);
      Scanner scanner = new Scanner(file);
      while (scanner.hasNextLine()) {
        String data = scanner.nextLine();
        lines.add(data);
      }
      scanner.close();
    } catch (FileNotFoundException e) {
      return nums;
    }

    for (int i = 0; i < lines.size(); i++) {
      String[] letters = lines.elementAt(i).split(",");
      for (int j = 0; j < letters.length; j++) {
        nums.add(Integer.parseInt(letters[j]));
      }
    }

    return nums;
  }
}
