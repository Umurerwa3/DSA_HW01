class SparseMatrix:
    def __init__(self, num_rows, num_cols):
        self.rows = num_rows
        self.cols = num_cols
        self.data = {}

    @staticmethod
    def from_file(file_path):
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()

            rows = int(lines[0][5:])
            cols = int(lines[1][5:])
            matrix = SparseMatrix(rows, cols)

            for line in lines[2:]:
                line = line.strip()
                if not line:
                    continue
                # Strip parentheses and split
                values = list(map(int, line[1:-1].split(",")))
                matrix.set_element(values[0], values[1], values[2])

            return matrix
        except Exception as e:
            raise Exception(f"Error reading file: {e}")

    def get_element(self, row, col):
        return self.data.get(row, {}).get(col, 0)

    def set_element(self, row, col, value):
        if value == 0:
            if row in self.data and col in self.data[row]:
                del self.data[row][col]
                if not self.data[row]:
                    del self.data[row]
        else:
            if row not in self.data:
                self.data[row] = {}
            self.data[row][col] = value

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition")

        result = SparseMatrix(self.rows, self.cols)

        for row in self.data:
            for col in self.data[row]:
                result.set_element(row, col, self.get_element(row, col))

        for row in other.data:
            for col in other.data[row]:
                current = result.get_element(row, col)
                result.set_element(row, col, current + other.get_element(row, col))

        return result

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for subtraction")

        result = SparseMatrix(self.rows, self.cols)

        for row in self.data:
            for col in self.data[row]:
                result.set_element(row, col, self.get_element(row, col))

        for row in other.data:
            for col in other.data[row]:
                current = result.get_element(row, col)
                result.set_element(row, col, current - other.get_element(row, col))

        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("Invalid dimensions for multiplication")

        result = SparseMatrix(self.rows, other.cols)

        for row1 in self.data:
            for col1 in self.data[row1]:
                val1 = self.data[row1][col1]
                if col1 in other.data:
                    for col2 in other.data[col1]:
                        val2 = other.data[col1][col2]
                        current = result.get_element(row1, col2)
                        result.set_element(row1, col2, current + val1 * val2)

        return result

    def __str__(self):
        result = f"rows={self.rows}\ncols={self.cols}\n"
        for row in sorted(self.data):
            for col in sorted(self.data[row]):
                value = self.data[row][col]
                result += f"({row}, {col}, {value})\n"
        return result


def main():
    import sys

    if len(sys.argv) < 5:
        print("Usage: python sparse_matrix.py <operation> <matrix1_file> <matrix2_file> <output_file>")
        return

    operation = sys.argv[1]
    file1 = sys.argv[2]
    file2 = sys.argv[3]
    output_file = sys.argv[4]

    try:
        matrix1 = SparseMatrix.from_file(file1)
        matrix2 = SparseMatrix.from_file(file2)

        if operation == "add":
            result = matrix1.add(matrix2)
        elif operation == "subtract":
            result = matrix1.subtract(matrix2)
        elif operation == "multiply":
            result = matrix1.multiply(matrix2)
        else:
            raise ValueError("Invalid operation. Use: add, subtract, or multiply")

        with open(output_file, "w") as out_file:
            out_file.write(str(result))
        print(f"Result written to {output_file}")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()