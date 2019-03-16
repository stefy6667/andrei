import java.util.Arrays;

public class DuplicateArray {

	public static void main(String[] args) {
		int[] numArray = { 1, 2, 3, 4, 5, 4, 3, 2, 6, 7, 8, 9 };
		int count = 0;
		Arrays.sort(numArray);

		System.out.println(Arrays.toString(numArray));
		for (int i = 0; i < numArray.length; i++) {
			for (int j = i + 1; j < numArray.length; j++)
				if (i != j && numArray[i] == numArray[j]) {
					count++;
				}

		}
		System.out.println(count);

	}

}
