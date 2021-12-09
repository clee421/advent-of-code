import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class Main {
  public static void main(String[] args) {
    var data = readFile("data-input");
    var result = solve(data);

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

  public Entry(String line) {
    // System.out.println(line);
    uniqSignalPatterns = new Vector<String>();
    digitalOutputs = new Vector<String>();
    mapping = new HashMap<String, Integer>();

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
    for (int i = 0; i < uniqSignalPatterns.size(); i++) {
      var signal = uniqSignalPatterns.elementAt(i);
      // System.out.println("working on " + signal + " element " + i);
      if (signal.length() == 7) {
        // have all letters is an 8
        mapping.put(signal, 8);
      } else if (signal.length() == 4) {
        mapping.put(signal, 4);
      } else if (signal.length() == 3) {
        mapping.put(signal, 7);
      } else if (signal.length() == 2) {
        mapping.put(signal, 1);
      }
    }
  }

  private String sort(String str) {
    char tempArray[] = str.toCharArray();
    Arrays.sort(tempArray);
    return new String(tempArray);
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
