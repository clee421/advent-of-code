import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class Main {
  public static void main(String[] args) {
    var data = readFile("data-input");
    var result = solve2(data);

    System.out.println("result: " + result);
  }

  private static long solve(Vector<Entry> entries) {
    int count = 0;
    for (int i = 0; i < entries.size(); i++) {
      var entry = entries.elementAt(i);
      // System.out.println("on row " + (i + 1));
      for (int j = 0; j < entry.digitalOutputs.size(); j++) {
        var seg = entry.digitalOutputs.elementAt(j);
        // System.out.println(seg + " has value " + entry.getValue(seg));
        if (
          entry.getValue(seg) == 1 ||
          entry.getValue(seg) == 4 ||
          entry.getValue(seg) == 7 ||
          entry.getValue(seg) == 8
        ) {
          count++;
        }
      }
    }

    return count;
  }

  private static long solve2(Vector<Entry> entries) {
    int sum = 0;
    for (int i = 0; i < entries.size(); i++) {
      var entry = entries.elementAt(i);
      // System.out.println("on row " + (i + 1));
      var row = "";
      for (int j = 0; j < entry.digitalOutputs.size(); j++) {
        var seg = entry.digitalOutputs.elementAt(j);
        // System.out.println(seg + " has value " + entry.getValue(seg));
        row += entry.getValue(seg);
      }

      System.out.println(row);
      sum += Integer.parseInt(row);
    }

    return sum;
  }

  private static Vector<Entry> readFile(String filename) {
    Vector<Entry> entries = new Vector<Entry>();
    try {
      File file = new File(filename);
      Scanner scanner = new Scanner(file);
      while (scanner.hasNextLine()) {
        String data = scanner.nextLine();
        var e = new Entry(data);
        // System.out.println(e.toString());
        entries.add(e);
      }
      scanner.close();
    } catch (FileNotFoundException e) {
      return entries;
    }

    return entries;
  }
}


class Entry {
  Vector<String> uniqSignalPatterns;
  Vector<String> digitalOutputs;

  private HashMap<String, Integer> mapping;
  private String[] reverseMap;

  public Entry(String line) {
    // System.out.println("\n" + line);
    uniqSignalPatterns = new Vector<String>();
    digitalOutputs = new Vector<String>();
    mapping = new HashMap<String, Integer>();
    reverseMap = new String[10];
    Arrays.fill(reverseMap, "");

    String[] segmentParts = line.split("\\|");
    // System.out.println("parts" + segmentParts[0] + " ? " + segmentParts[1]);
    var usp = segmentParts[0].trim().split(" ");
    for (int i = 0; i < usp.length; i++) {
      // System.out.println(usp[i]);
      uniqSignalPatterns.add(sort(usp[i]));
    }

    var digo = segmentParts[1].trim().split(" ");
    for (int i = 0; i < digo.length; i++) {
      digitalOutputs.add(sort(digo[i]));
    }

    calculateMapping();
  }

  public String toString() {
    return uniqSignalPatterns.toString() + " :: " + digitalOutputs.toString();
  }

  public int getValue(String segment) {
    var val = mapping.get(segment);
    if (val == null) {
      return -1;
    }

    return val;
  }

  private void calculateMapping() {
    // find 1, 4, 7, 8
    for (int i = 0; i < uniqSignalPatterns.size(); i++) {
      // System.out.println("\ncalc mapping on index " + i);
      var signal = uniqSignalPatterns.elementAt(i);
      // System.out.println("working on " + signal + " element " + i);

      if (signal.length() == 7) {
        // have all letters is an 8
        // System.out.println("found " + signal + " to be 8");
        mapping.put(signal, 8);
        reverseMap[8] = signal;
        uniqSignalPatterns.removeElementAt(i);
        i -= 1;
      } else if (signal.length() == 4) {
        // System.out.println("found " + signal + " to be 4");
        mapping.put(signal, 4);
        reverseMap[4] = signal;
        uniqSignalPatterns.removeElementAt(i);
        i -= 1;
      } else if (signal.length() == 3) {
        // System.out.println("found " + signal + " to be 7");
        mapping.put(signal, 7);
        reverseMap[7] = signal;
        uniqSignalPatterns.removeElementAt(i);
        i -= 1;
      } else if (signal.length() == 2) {
        // System.out.println("found " + signal + " to be 1");
        mapping.put(signal, 1);
        reverseMap[1] = signal;
        uniqSignalPatterns.removeElementAt(i);
        i -= 1;
      }
    }

    // find 9, which overlaps with 4 & 7
    for (int i = 0; i < uniqSignalPatterns.size(); i++) {
      var signal = uniqSignalPatterns.elementAt(i);
      if (
        signal.length() == 6 &&
        similarityScore(signal, reverseMap[4]) == 4 &&
        similarityScore(signal, reverseMap[7]) == 3
      ) {
        // System.out.println("found " + signal + " to be 9");
        mapping.put(signal, 9);
        reverseMap[9] = signal;
        uniqSignalPatterns.removeElementAt(i);
      }
    }

    // find 0, which overlaps with 7
    for (int i = 0; i < uniqSignalPatterns.size(); i++) {
      var signal = uniqSignalPatterns.elementAt(i);
      if (
        signal.length() == 6 &&
        similarityScore(signal, reverseMap[7]) == 3
      ) {
        // System.out.println("found " + signal + " to be 0");
        mapping.put(signal, 0);
        reverseMap[0] = signal;
        uniqSignalPatterns.removeElementAt(i);
      }
    }

    // find 6, which at this point is the only one left with 6 length
    for (int i = 0; i < uniqSignalPatterns.size(); i++) {
      var signal = uniqSignalPatterns.elementAt(i);
      if (signal.length() == 6) {
        // System.out.println("found " + signal + " to be 6");
        mapping.put(signal, 6);
        reverseMap[6] = signal;
        uniqSignalPatterns.removeElementAt(i);
      }
    }

    // find 3, which overlaps with 9 & 7
    for (int i = 0; i < uniqSignalPatterns.size(); i++) {
      var signal = uniqSignalPatterns.elementAt(i);
      if (
        signal.length() == 5 &&
        similarityScore(signal, reverseMap[7]) == 3 &&
        similarityScore(signal, reverseMap[9]) == 5
      ) {
        // System.out.println("found " + signal + " to be 3");
        mapping.put(signal, 3);
        reverseMap[3] = signal;
        uniqSignalPatterns.removeElementAt(i);
      }
    }

    // find 5, which overlaps with 9
    for (int i = 0; i < uniqSignalPatterns.size(); i++) {
      var signal = uniqSignalPatterns.elementAt(i);
      if (signal.length() == 5 && similarityScore(signal, reverseMap[9]) == 5) {
        // System.out.println("found " + signal + " to be 5");
        mapping.put(signal, 5);
        reverseMap[5] = signal;
        uniqSignalPatterns.removeElementAt(i);
      }
    }

    if (uniqSignalPatterns.size() != 1) {
      System.out.println(uniqSignalPatterns);
      System.err.println("wtf something broke");
      System.exit(1);
    }

    // 2 is left
    var signal = uniqSignalPatterns.elementAt(0);
    // System.out.println("found " + signal + " to be 2");
    mapping.put(signal, 2);
    reverseMap[2] = signal;
    uniqSignalPatterns.removeElementAt(0);
  }

  private String sort(String str) {
    char tempArray[] = str.toCharArray();
    Arrays.sort(tempArray);
    return new String(tempArray);
  }

  private int similarityScore(String left, String right) {
    int score = 0;
    var map = new HashSet<Character>();

    var leftArray = left.toCharArray();
    for (int i = 0; i < leftArray.length; i++) {
      map.add(leftArray[i]);
    }

    var rightArray = right.toCharArray();
    for (int i = 0 ; i < rightArray.length; i++) {
      if (map.contains(rightArray[i])) {
        score++;
      }
    }

    return score;
  }
}

// class Segment {
//   Set<String> uniqLetters;

//   public Segment(String letters) {
//   //  System.out.println(letters);
//     uniqLetters = new HashSet<String>();
//     for (int i = 0; i < letters.length(); i++) {
//       uniqLetters.add(String.valueOf(letters.charAt(i)));
//     }
//   }

//   public String toString() {
//     return String.join("-", uniqLetters);
//   }

//   // useless
//   public int getValue() {
//     // has all letters
//     if (
//       uniqLetters.contains("a") &&
//       uniqLetters.contains("b") &&
//       uniqLetters.contains("c") &&
//       uniqLetters.contains("d") &&
//       uniqLetters.contains("e") &&
//       uniqLetters.contains("f") &&
//       uniqLetters.contains("g") &&
//       uniqLetters.size() == 7
//     ) {
//       return 8;
//     }

//     // missing 1 letter
//     if (
//       uniqLetters.contains("a") &&
//       uniqLetters.contains("b") &&
//       uniqLetters.contains("c") &&
//       uniqLetters.contains("e") &&
//       uniqLetters.contains("f") &&
//       uniqLetters.contains("g") &&
//       uniqLetters.size() == 6
//     ) {
//       return 0;
//     }

//     if (
//       uniqLetters.contains("a") &&
//       uniqLetters.contains("b") &&
//       uniqLetters.contains("d") &&
//       uniqLetters.contains("e") &&
//       uniqLetters.contains("f") &&
//       uniqLetters.contains("g") &&
//       uniqLetters.size() == 6
//     ) {
//       return 6;
//     }

//     if (
//       uniqLetters.contains("a") &&
//       uniqLetters.contains("b") &&
//       uniqLetters.contains("c") &&
//       uniqLetters.contains("d") &&
//       uniqLetters.contains("f") &&
//       uniqLetters.contains("g") &&
//       uniqLetters.size() == 6
//     ) {
//       return 9;
//     }

//     // missing 2 letters
//     if (
//       uniqLetters.contains("a") &&
//       uniqLetters.contains("c") &&
//       uniqLetters.contains("d") &&
//       uniqLetters.contains("e") &&
//       uniqLetters.contains("g") &&
//       uniqLetters.size() == 5
//     ) {
//       return 2;
//     }

//     if (
//       uniqLetters.contains("a") &&
//       uniqLetters.contains("c") &&
//       uniqLetters.contains("d") &&
//       uniqLetters.contains("f") &&
//       uniqLetters.contains("g") &&
//       uniqLetters.size() == 5
//     ) {
//       return 3;
//     }

//     if (
//       uniqLetters.contains("a") &&
//       uniqLetters.contains("b") &&
//       uniqLetters.contains("d") &&
//       uniqLetters.contains("f") &&
//       uniqLetters.contains("g") &&
//       uniqLetters.size() == 5
//     ) {
//       return 5;
//     }

//     // missing 3 letters
//     if (
//       uniqLetters.contains("b") &&
//       uniqLetters.contains("c") &&
//       uniqLetters.contains("d") &&
//       uniqLetters.contains("f") &&
//       uniqLetters.size() == 4
//     ) {
//       return 4;
//     }

//     // rest
//     if (
//       uniqLetters.contains("a") &&
//       uniqLetters.contains("c") &&
//       uniqLetters.contains("f") &&
//       uniqLetters.size() == 3
//     ) {
//       return 7;
//     }

//     if (
//       uniqLetters.contains("c") &&
//       uniqLetters.contains("f") &&
//       uniqLetters.size() == 2
//     ) {
//       return 1;
//     }

//     return -1;
//   }

//   public Boolean isDigit() {
//     return getValue() != -1;
//   }
// }
