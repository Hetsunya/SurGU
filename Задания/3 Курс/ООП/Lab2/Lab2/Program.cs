namespace Lab2
{
    internal class Program
    {
        public class Square
        {
            private double sideLength;

            public Square(double sideLength)
            {
                this.sideLength = sideLength;
            }

            public double CalculatePerimeter()
            {
                return 4 * sideLength;
            }

            public double CalculateArea()
            {
                return sideLength * sideLength;
            }
        }

        public class Cylinder
        {
            private double radius;
            private double height;

            public Cylinder(double radius, double height)
            {
                this.radius = radius;
                this.height = height;
            }

            public double CalculateVolume()
            {
                return Math.PI * radius * radius * height;
            }

            public double CalculateSurfaceArea()
            {
                double baseArea = Math.PI * radius * radius;
                double lateralArea = 2 * Math.PI * radius * height;
                return 2 * baseArea + lateralArea;
            }
        }

        static void Main(string[] args)
        {
            double sideLength, radius, height;

            // Ввод параметров квадрата
            Console.Write("Введите длину стороны квадрата: ");
            if (!double.TryParse(Console.ReadLine(), out sideLength) || sideLength <= 0)
            {
                Console.WriteLine("Некорректный ввод. Длина стороны квадрата должна быть положительным числом.");
                return;
            }

            // Создаем квадрат
            Square square = new Square(sideLength);

            // Выводим результаты для квадрата
            double squarePerimeter = square.CalculatePerimeter();
            double squareArea = square.CalculateArea();

            Console.WriteLine("Квадрат:");
            Console.WriteLine($"Периметр: {squarePerimeter}");
            Console.WriteLine($"Площадь: {squareArea}");

            // Ввод параметров цилиндра
            Console.Write("Введите радиус цилиндра: ");
            if (!double.TryParse(Console.ReadLine(), out radius) || radius <= 0)
            {
                Console.WriteLine("Некорректный ввод. Радиус цилиндра должен быть положительным числом.");
                return;
            }

            Console.Write("Введите высоту цилиндра: ");
            if (!double.TryParse(Console.ReadLine(), out height) || height <= 0)
            {
                Console.WriteLine("Некорректный ввод. Высота цилиндра должна быть положительным числом.");
                return;
            }

            // Создаем цилиндр
            Cylinder cylinder = new Cylinder(radius, height);

            // Выводим результаты для цилиндра
            double cylinderVolume = cylinder.CalculateVolume();
            double cylinderSurfaceArea = cylinder.CalculateSurfaceArea();

            Console.WriteLine("Цилиндр:");
            Console.WriteLine($"Объем: {cylinderVolume}");
            Console.WriteLine($"Площадь поверхности: {cylinderSurfaceArea}");

            Console.ReadLine();
        }

    }
}