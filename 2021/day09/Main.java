import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class Main {
  public static void main(String[] args) {
    var data = readFile("data-test");
    var result = solve(data);

    System.out.println("result: " + result);
  }

  private static long solve(HeightMap map) {
    int sum = 0;
    for (int i = 0; i < map.map.size(); i++) {
      for (int j = 0; j < map.map.elementAt(i).size(); j++) {
        var num = map.map.elementAt(i).elementAt(j);
        var surround = map.getSurrounding(i, j);
        if (isMin(num, surround)) {
          System.out.println("min " + i + " - " + j + " -> " + num);
          sum += (num + 1);
        }
      }
    }
    return sum;
  }

  private static Boolean isMin(int n, Integer[] nums) {
    for (int i = 0; i < nums.length; i++) {
      if (nums[i] <= n) {
        // System.out.println("nums[i] >= n " + Arrays.toString(nums) + " - " + n);
        return false;
      }
    }

    return true;
  }

  private static HeightMap readFile(String filename) {
    var map = new HeightMap();
    try {
      File file = new File(filename);
      Scanner scanner = new Scanner(file);
      while (scanner.hasNextLine()) {
        String data = scanner.nextLine();
        map.add(data);
      }
      scanner.close();
    } catch (FileNotFoundException e) {
      return map;
    }

    return map;
  }
}

class HeightMap {
  Vector<Vector<Integer>> map;

  public HeightMap() {
    map = new Vector<Vector<Integer>>();
  }

  public void add(String line) {
    map.add(parse(line));
  }

  public Integer[] getSurrounding(int x, int y) {
    Vector<Integer> around = new Vector<Integer>();
    // up
    int nx = x - 1;
    int ny = y;
    if (0 <= nx && nx < map.size()) {
      around.add(map.elementAt(nx).elementAt(ny));
    }

    // down
    nx = x + 1;
    ny = y;
    if (0 <= nx && nx < map.size()) {
      around.add(map.elementAt(nx).elementAt(ny));
    }

    // left
    nx = x;
    ny = y - 1;
    if (0 <= ny && ny < map.elementAt(nx).size()) {
      around.add(map.elementAt(nx).elementAt(ny));
    }

    // right
    nx = x;
    ny = y + 1;
    if (0 <= ny && ny < map.elementAt(nx).size()) {
      around.add(map.elementAt(nx).elementAt(ny));
    }

    return around.toArray(new Integer[around.size()]);
  }

  private Vector<Integer> parse(String line) {
    var row = new Vector<Integer>();
    for (int i = 0; i < line.length(); i++) {
      var l = line.charAt(i);
      row.add(Character.getNumericValue(l));
    }

    return row;
  }
}