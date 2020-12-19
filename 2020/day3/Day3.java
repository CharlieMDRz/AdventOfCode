import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class Day3 {
public String fileName;

public int horizontalIncrement;
public int verticalIncrement;

    public Day3(String fileName, int horizontalIncrement, int verticalIncrement) {
    this.fileName = fileName;
        this.horizontalIncrement = horizontalIncrement;
        this.verticalIncrement = verticalIncrement;
    }

    public int main() {
        Path filePath = FileSystems.getDefault().getPath(fileName);
        Charset charset = StandardCharsets.UTF_8;
        List<String> lines;

        int treeHitCount = 0;
        int position = 0;

        try {
            lines = Files.readAllLines(filePath, charset);
            // for(String line : lines) {
            for (int index = 0; index < lines.size(); index++) {
                String line = lines.get(index);
                // if (lines.indexOf(line) % verticalIncrement == 0) {
                if (index % verticalIncrement == 0) {
                    if (line.charAt(position % line.length()) == '#') {
                        treeHitCount++;
                     }
                    position += horizontalIncrement;
                 }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return treeHitCount;
    }

    public static void main(String[] args) {
        System.out.println(args[0]);
        Day3 slide = new Day3(args[0], Integer.parseInt(args[1]), Integer.parseInt(args[2]));
        System.out.println(slide.main());
    }
}
