class SparseMatrix:
    def __init__(self, num_rows, num_cols):
        # Initialize matrix with given dimensions
        self.rows = num_rows
        self.cols = num_cols
        self.data = {}  # Store non-zero values only using nested dictionary

    @staticmethod
    def from_file(file_path):
        # Read matrix data from a file and return a SparseMatrix object
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()

            # Read number of rows and columns from the first two lines
            rows = int(lines[0][5:])
            cols = int(lines[1][5:])
            matrix = SparseMatrix(rows, cols)

            # Read each non-zero entry and add it to the matrix
            for line in lines[2:]:
                line = line.strip()
                if not line:
                    continue
                # Remove parentheses and split the line into integers
                values = list(map(int, line[1:-1].split(",")))
                matrix.set_element(values[0], values[1], values[2])

            return matrix
        except Exception as e:
            raise Exception(f"Error reading file: {e}")

    def get_element(self, row, col):
        # Get the value at a specific row and column (return 0 if not set)
        return self.data.get(row, {}).get(col, 0)

    def set_element(self, row, col, value):
        # Set the value at a specific row and column
        if value == 0:
            # Remove the element if it's zero
            if row in self.data and col in self.data[row]:
                del self.data[row][col]
                if not self.data[row]:
                    del self.data[row]
        else:
            # Add or update the element
            if row not in self.data:
                self.data[row] = {}
            self.data[row][col] = value

    def add(self, other):
        # Add two matrices and return the result
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition")

        result = SparseMatrix(self.rows, self.cols)

        # Add elements from the first matrix
        for row in self.data:
            for col in self.data[row]:
                result.set_element(row, col, self.get_element(row, col))

        # Add elements from the second matrix
        for row in other.data:
            for col in other.data[row]:
                current = result.get_element(row, col)
                result.set_element(row, col, current + other.get_element(row, col))

        return result

    def subtract(self, other):
        # Subtract another matrix from this matrix and return the result
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for subtraction")

        result = SparseMatrix(self.rows, self.cols)

        # Copy elements from the first matrix
        for row in self.data:
            for col in self.data[row]:
                result.set_element(row, col, self.get_element(row, col))

        # Subtract elements from the second matrix
        for row in other.data:
            for col in other.data[row]:
                current = result.get_element(row, col)
                result.set_element(row, col, current - other.get_element(row, col))

        return result

    def multiply(self, other):
        # Multiply this matrix with another matrix and return the result
        if self.cols != other.rows:
            raise ValueError("Invalid dimensions for multiplication")

        result = SparseMatrix(self.rows, other.cols)

        # Multiply non-zero elements only
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
        # Convert the matrix to a string format for printing or saving to file
        result = f"rows={self.rows}\ncols={self.cols}\n"
        for row in sorted(self.data):
            for col in sorted(self.data[row]):
                value = self.data[row][col]
                result += f"({row}, {col}, {value})\n"
        return result


def main():
    import sys

    # Check for correct number of arguments
    if len(sys.argv) < 5:
        print("Usage: python sparse_matrix.py <operation> <matrix1_file> <matrix2_file> <output_file>")
        return

    # Get operation and file names from command line arguments
    operation = sys.argv[1]
    file1 = sys.argv[2]
    file2 = sys.argv[3]
    output_file = sys.argv[4]

    try:
        # Load matrices from the given files
        matrix1 = SparseMatrix.from_file(file1)
        matrix2 = SparseMatrix.from_file(file2)

        # Perform the specified operation
        if operation == "add":
            result = matrix1.add(matrix2)
        elif operation == "subtract":
            result = matrix1.subtract(matrix2)
        elif operation == "multiply":
            result = matrix1.multiply(matrix2)
        else:
            raise ValueError("Invalid operation. Use: add, subtract, or multiply")

        # Write the result to the output file
        with open(output_file, "w") as out_file:
            out_file.write(str(result))
        print(f"Result written to {output_file}")

    except Exception as e:
        print("Error:", e)


# Run the main function if this file is executed directly
if __name__ == "__main__":
    main()
