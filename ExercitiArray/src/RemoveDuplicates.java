import java.util.Arrays;

public class RemoveDuplicates {
	public static void main(String[] args) {
		int[] numArray = { 1, 2, 3, 4, 5, 4, 3, 2, 6, 7, 8, 9, 5, 6, 7 };
		int[] duplicates = new int[numArray.length];

		Arrays.sort(numArray);
		System.out.println(Arrays.toString(numArray));
		for (int i = 0; i < numArray.length; i++) {
			for (int j = i + 1; j < numArray.length; j++)
				if (i != j && numArray[i] == numArray[j]) {

					duplicates[i] = numArray[i];

				}
			numArray[i] = numArray[i] - duplicates[i];

		}
		System.out.println(Arrays.toString(numArray));
	}

}
