namespace GLMS.Web.Services
{
    public interface IFileService
    {
        bool IsValidPdf(IFormFile file);
        Task<string> SaveFileAsync(IFormFile file, string uploadFolder);
    }

    public class FileService : IFileService
    {
        private static readonly string[] AllowedExtensions = { ".pdf" };
        private const long MaxFileSizeBytes = 5 * 1024 * 1024;

        public bool IsValidPdf(IFormFile file)
        {
            if (file == null || file.Length == 0) return false;
            var ext = Path.GetExtension(file.FileName).ToLowerInvariant();
            if (!AllowedExtensions.Contains(ext)) return false;
            if (file.Length > MaxFileSizeBytes) return false;
            return true;
        }

        public async Task<string> SaveFileAsync(IFormFile file, string uploadFolder)
        {
            Directory.CreateDirectory(uploadFolder);
            var uniqueName = $"{Guid.NewGuid()}_{Path.GetFileName(file.FileName)}";
            using var stream = new FileStream(Path.Combine(uploadFolder, uniqueName), FileMode.Create);
            await file.CopyToAsync(stream);
            return uniqueName;
        }
    }
}
