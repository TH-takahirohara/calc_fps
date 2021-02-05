# coding:utf-8
from matplotlib import pyplot as plt
import re
import sys

def output_processing_time():
  all_arr = []
  seg_arr = []
  draw_arr = []

  # グラフ出力および平均値計算に用いる測定点数
  sample_num = 500
  # プロットのy軸最大値
  y_limit = 500

  args = sys.argv
  if len(args) == 1:
    print("コマンドライン引数としてログファイル名を渡してください")
    return

  data = open(args[1], 'r')

  for line in data:
    all_time = re.findall(r'all: (.+) ms', line)
    seg_time = re.findall(r'segment: (.+) ms', line)
    draw_time = re.findall(r'draw: (.+) ms', line)
    if all_time:
      if len(all_arr) < sample_num + 1:
        all_arr.append(float(all_time[0]))
    elif seg_time:
      if len(seg_arr) < sample_num + 1:
        seg_arr.append(float(seg_time[0]))
    elif draw_time:
      if len(draw_arr) < sample_num + 1:
        draw_arr.append(float(draw_time[0]))

  if len(all_arr) < sample_num + 1 or len(seg_arr) < sample_num + 1 or len(draw_arr) < sample_num + 1:
    print("設定した測定点数よりもログのデータ数が少ないです。\n測定点数の設定(sample_num)を変更してください。")
    return
  
  # 処理時間平均値およびfps
  all_ave = sum(all_arr) / len(all_arr)
  print("all ave:", all_ave, "ms")
  print("segment ave:", sum(seg_arr) / len(seg_arr), "ms")
  print("draw ave:", sum(draw_arr) / len(draw_arr), "ms")
  print("fps:", 1000 / all_ave)

  # 最初の計測結果を除いた場合の処理時間平均値およびfps
  all_ave_wo_first = sum(all_arr[1:]) / len(all_arr[1:])
  print("all ave(w/o first):", all_ave_wo_first, "ms")
  print("segment ave(w/o first):", sum(seg_arr[1:]) / len(seg_arr[1:]), "ms")
  print("draw ave(w/o first):", sum(draw_arr[1:]) / len(draw_arr[1:]), "ms")
  print("fps(w/o first):", 1000 / all_ave_wo_first)

  filename_wo_ext = args[1].split('/')[-1].split('.')[0]

  # 平均値データのtxtファイルへの出力
  output_path = f'output_files/{filename_wo_ext}_ave.txt'
  with open(output_path, mode='w') as f:
    f.write('all ave: {} ms\n'.format(all_ave))
    f.write('segment ave: {} ms\n'.format(sum(seg_arr) / len(seg_arr)))
    f.write('draw ave: {} ms\n'.format(sum(draw_arr) / len(draw_arr)))
    f.write('fps: {}\n\n'.format(1000 / all_ave))
    f.write('all ave(w/o first): {} ms\n'.format(all_ave_wo_first))
    f.write('segment ave(w/o first): {} ms\n'.format(sum(seg_arr[1:]) / len(seg_arr[1:])))
    f.write('draw ave(w/o first): {} ms\n'.format(sum(draw_arr[1:]) / len(draw_arr[1:])))
    f.write('fps(w/o first): {}\n'.format(1000 / all_ave_wo_first))

  # グラフの描画
  fig = plt.figure()
  plt.plot(list(range(len(all_arr))), all_arr)
  plt.plot(list(range(len(seg_arr))), seg_arr)
  plt.plot(list(range(len(draw_arr))), draw_arr)
  plt.xlim(-30, sample_num + 30)
  plt.ylim(0, y_limit)
  plt.xlabel("Measurement number")
  plt.ylabel("Processing time [ms]")
  plt.legend(["all", "segment", "draw"])
  plt.show()

  # グラフの保存
  fig.savefig(f'images/{filename_wo_ext}.png')

output_processing_time()
