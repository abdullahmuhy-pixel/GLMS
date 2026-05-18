using GLMS.Web.Services;
using Microsoft.AspNetCore.Http;
using System.Text;
using Xunit;
namespace GLMS.Tests
{
    public class FileValidationTests
    {
        private readonly FileService _fileService = new FileService();

        private IFormFile CreateMockFile(string fileName, string content = "fake content")
        {
            var bytes = Encoding.UTF8.GetBytes(content);
            var stream = new MemoryStream(bytes);
            return new FormFile(stream, 0, bytes.Length, "file", fileName)
            { Headers = new HeaderDictionary(), ContentType = "application/octet-stream" };
        }

        [Fact] public void IsValidPdf_ValidPdfFile_ReturnsTrue()
        { Assert.True(_fileService.IsValidPdf(CreateMockFile("contract.pdf"))); }

        [Fact] public void IsValidPdf_ExeFile_ReturnsFalse()
        { Assert.False(_fileService.IsValidPdf(CreateMockFile("malware.exe"))); }

        [Fact] public void IsValidPdf_DocxFile_ReturnsFalse()
        { Assert.False(_fileService.IsValidPdf(CreateMockFile("contract.docx"))); }

        [Fact] public void IsValidPdf_JpgFile_ReturnsFalse()
        { Assert.False(_fileService.IsValidPdf(CreateMockFile("photo.jpg"))); }

        [Fact] public void IsValidPdf_NullFile_ReturnsFalse()
        { Assert.False(_fileService.IsValidPdf(null!)); }

        [Fact] public void IsValidPdf_EmptyFile_ReturnsFalse()
        {
            var stream = new MemoryStream(Array.Empty<byte>());
            Assert.False(_fileService.IsValidPdf(new FormFile(stream, 0, 0, "file", "empty.pdf")));
        }

        [Fact] public void IsValidPdf_UpperCasePdf_ReturnsTrue()
        { Assert.True(_fileService.IsValidPdf(CreateMockFile("CONTRACT.PDF"))); }

        [Fact] public void IsValidPdf_MixedCasePdf_ReturnsTrue()
        { Assert.True(_fileService.IsValidPdf(CreateMockFile("doc.Pdf"))); }

        [Fact] public void IsValidPdf_TxtFile_ReturnsFalse()
        { Assert.False(_fileService.IsValidPdf(CreateMockFile("notes.txt"))); }

        [Fact] public void IsValidPdf_NoExtension_ReturnsFalse()
        { Assert.False(_fileService.IsValidPdf(CreateMockFile("contractfile"))); }
    }
}
