import java.util.Arrays;

public class RangeArray {

	public static void main(String[] args) {
		int[] myArr = { 1, 2, 3, 4, 5 };
		int a = 0;
		int b = 0;
		Arrays.sort(myArr);
		for (int i = 0; i < myArr.length; i++) {
			if (i == 0) {
				a = myArr[i];
			}
			if (i == myArr.length - 1) {
				b = myArr[i];
			}
		}
		System.out.println("The range of array element is " + a + " to " + b);

	}

}
