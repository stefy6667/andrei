import java.util.Arrays;

public class Max1Max2 {
	public static void main(String[] args) {
		int[] numArray = { 1, 2, 3, 4, 5, 4, 3, 2, 6, 7, 8, 9, 5, 6, 7 };
		int max1 = 1;
		int max2 = 1;
		Arrays.sort(numArray);
		for (int i = 0; i < numArray.length; i++) {
			if (numArray[i] > max1) {
				max2 = max1;
				max1 = numArray[i];

			} else if (numArray[i] > max2) {
				max2 = numArray[i];
			}

		}
		System.out.println(max1);
		System.out.println(max2);
	}

}
