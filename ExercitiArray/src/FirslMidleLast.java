import java.util.Arrays;

public class FirslMidleLast {
	public static void main(String[] args) {
		int[] myArr = { 1, 2, 3, 4, 5, 9, 7, 6, 8 };
		int first = 0;
		int middle = 0;
		int last = 0;
		Arrays.sort(myArr);
		for (int i = 0; i < myArr.length; i++) {
			if (i == 0) {
				first = myArr[i];
			} else if (i == myArr.length / 2) {
				middle = myArr[i];
			} else if (i == myArr.length - 1) {
				last = myArr[i];
			}

		}
		System.out.println("First is " + first + " middle is " + middle + " last is " + last);
	}

}
