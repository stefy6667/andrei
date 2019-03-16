import java.util.Arrays;

public class LargeAndSmal {
	public static void main(String[] args) {
		int[] numArray = { 1, 2, 3, 4, 5, 4, 3, 2, 6, 7, 8, 9, 5, 6, 7, 10 };
		Arrays.sort(numArray);
		for (int i = 0; i < numArray.length; i++) {
			if (i == 0) {
				System.out.println(numArray[i]);
			}
			if (i == numArray.length - 1) {
				System.out.println(numArray[i]);
			}
		}
	}

}
