import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class Main {
  public static void main(String[] args) {
    var nums = readFile("data-input");
    var result = solve(nums, 256);

    System.out.println("Fishes: " + result);
  }

  private static long solve(Vector<Integer> fishes, int days) {
    long[] bucket = {0, 0, 0, 0, 0, 0, 0, 0, 0};

    for (int i = 0; i < fishes.size(); i++) {
      int d = fishes.elementAt(i);
      bucket[d]++;
    }

    for (int i = 0; i < days; i++) {
      long birthFish = bucket[0];
      for (int b = 0; b < bucket.length - 1; b++) {

        bucket[b] = bucket[b + 1];
      }

      bucket[8] = birthFish;
      bucket[6] += birthFish;
    }

    long sum = 0;
    for (int i = 0; i < bucket.length; i++) {
      sum += bucket[i];
    }

    return sum;
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
