public class Playground {
  public static void main(String[] args) {
    String text = "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe";
    var p = text.split("\\|");
    System.out.println(p[0]);
  }

}
