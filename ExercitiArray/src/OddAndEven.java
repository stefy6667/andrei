
public class OddAndEven {
	public static void main(String[] args) {
		int[] myArray = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
		int odd = 0;
		int even = 0;
		for (int i = 0; i < myArray.length; i++) {
			if (myArray[i] % 2 == 0) {
				odd++;
			} else if (myArray[i] % 2 != 0) {
				even++;
			}

		}
		System.out.println("On arrray is " + odd + " Odd element and " + even + " Even elements");
	}

}
