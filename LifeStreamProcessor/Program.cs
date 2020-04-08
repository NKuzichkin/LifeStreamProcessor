using FFmpeg.AutoGen;
using m3uParser;
using System;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using YoutubeExplode;

namespace LifeStreamProcessor
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            var httpClient = new HttpClient();
            var client = new YoutubeClient();
            var video = await client.GetVideoMediaStreamInfosAsync("BNKymFTrNL4");

            if(!Directory.Exists(@"tmp"))
            {
                Directory.CreateDirectory(@"tmp");
            }

            if(video?.HlsLiveStreamUrl != null)
            {
                var indexPlayList = await httpClient.GetStringAsync(video.HlsLiveStreamUrl!);
                var parser = new M3u8Parser.M3u8Parser();
                parser.Load(indexPlayList);
                var sorcesInfo = await parser.Parse();
                var targetSource = sorcesInfo.OrderByDescending(x => x.Resolution.Height * x.Resolution.Width).FirstOrDefault();
                var segmentPlayList = await httpClient.GetStringAsync(targetSource.Url!);
                var segmentsCandidates = Regex.Split(segmentPlayList, @"#EXTINF:\d\.\d\d\d,");
                var segmentUrl = segmentsCandidates.Skip(2).FirstOrDefault().Trim();
                var segmentBytes = await httpClient.GetByteArrayAsync(segmentUrl);
                var newFilename = Guid.NewGuid();
                var newFileNameLong = $"tmp/{newFilename}.ts";
                await File.WriteAllBytesAsync(newFileNameLong, segmentBytes);
            }
        }
    }
}
