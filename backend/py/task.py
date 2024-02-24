from dataclasses import dataclass
from heapq import nsmallest

@dataclass
class File:
    id: int
    name: str
    categories: list[str]
    parent: int
    size: int

# Note: Assume that ids are unique for all files and cannot be negative
#  but that other properties may be duplicated

"""
Task 1
"""
# Note: Assume that if two files have the same name, and one is a leaf node
#  but the other isn't, that the name should still be returned once
def leafFiles(files: list[File]) -> list[str]:
    # Initialise dictionary that maps file ids to names to allow O(1) removal
    leafFileIdToName = {}
    for file in files:
        leafFileIdToName[file.id] = file.name

    # Remove all parent files from dictionary
    for file in files:
        # Ensures that the parent isn't -1 and hasn't already been removed
        if file.parent in leafFileIdToName:
            leafFileIdToName.pop(file.parent)

    # leafFileIdToName now only contains leaf files
    return leafFileIdToName.values()


"""
Task 2
"""
# Note: Assume that it is fine to use the Python standard library
def kLargestCategories(files: list[File], k: int) -> list[str]:
    # Maps each category to the amount of files it has
    categories = {}

    for file in files:
        for category in file.categories:
            categories[category] = categories.get(category, 0) + 1
    
    # Used to sort the categories into descending order by file count, 
    # but into ascending alphabetical order as a second priority
    def evaluateCategory(categoryItem):
        categoryName, fileCount = categoryItem
        return (-fileCount, categoryName)

    largestCategoryItems = nsmallest(k, categories.items(), key=evaluateCategory)
    return [categoryItem[0] for categoryItem in largestCategoryItems]


"""
Task 3
"""
# Note: assume the filesystem graph is acyclic (ie within context,
#  a folder cannot contain a symlink to one of its ancestor folders)
# If this could not be guranteed then this implementation wouldn't work
def largestFileSize(files: list[File]) -> int:
    # Maps file id to a set of the ids of each of its children
    # Note that it has a dummy head of an imaginary "root file" of id -1
    childrenOfFile = {}

    idToFile = {} # Maples file id to its object

    for file in files:
        idToFile[file.id] = file
        
        if file.parent in childrenOfFile:
            childrenOfFile[file.parent].add(file.id)
        else:
            childrenOfFile[file.parent] = {file.id}
    
    # Note: Assume that there aren't files nested deeper than python's recursion limit,
    # if there were, an iterative solution (using a stack) would be better
    
    def getFileSize(fileId):
        fileSize = idToFile[fileId].size
        for child in childrenOfFile.get(fileId, []):
            fileSize += getFileSize(child)

        return fileSize
    
    # Note: Assume all file sizes are positive
    largestFileSizeSoFar = 0
    for rootFileId in childrenOfFile[-1]:
        fileSize = getFileSize(rootFileId)
        if fileSize > largestFileSizeSoFar:
            largestFileSizeSoFar = fileSize
        

    return largestFileSizeSoFar


if __name__ == '__main__':
    testFiles = [
        File(1, "Document.txt", ["Documents"], 3, 1024),
        File(2, "Image.jpg", ["Media", "Photos"], 34, 2048),
        File(3, "Folder", ["Folder"], -1, 0),
        File(5, "Spreadsheet.xlsx", ["Documents", "Excel"], 3, 4096),
        File(8, "Backup.zip", ["Backup"], 233, 8192),
        File(13, "Presentation.pptx", ["Documents", "Presentation"], 3, 3072),
        File(21, "Video.mp4", ["Media", "Videos"], 34, 6144),
        File(34, "Folder2", ["Folder"], 3, 0),
        File(55, "Code.py", ["Programming"], -1, 1536),
        File(89, "Audio.mp3", ["Media", "Audio"], 34, 2560),
        File(144, "Spreadsheet2.xlsx", ["Documents", "Excel"], 3, 2048),
        File(233, "Folder3", ["Folder"], -1, 4096),
    ]

    assert sorted(leafFiles(testFiles)) == [
        "Audio.mp3",
        "Backup.zip",
        "Code.py",
        "Document.txt",
        "Image.jpg",
        "Presentation.pptx",
        "Spreadsheet.xlsx",
        "Spreadsheet2.xlsx",
        "Video.mp4"
    ]

    assert kLargestCategories(testFiles, 3) == [
        "Documents", "Folder", "Media"
    ]

    assert largestFileSize(testFiles) == 20992
