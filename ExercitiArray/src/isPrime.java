
public class isPrime {

	public static void main(String[] args) {
		int a = 4;
		boolean prime = true;
		for (int i = 2; i <= a / 2; i++) {
			if (a % i == 0) {
				prime = false;
			}
		}
		System.out.println("is prime? " + prime);

	}

}
