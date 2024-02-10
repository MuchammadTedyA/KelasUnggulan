from django.shortcuts import render,  redirect, get_object_or_404
from django.core.paginator import Paginator
import xlwt
from django.http import HttpResponse
# from .formSiswa import dataSiswa
from django.http import JsonResponse
from .models import siswa, kriteria, sub_kriteria, bobot_kriteria_ahp, sum_kriteria_ahp, skala_fuzzy, skala_fuzzy2, bobot_kriteria_fahp, sum_kriteria_fahp, derajat_probabilitas, bobot_subkriteria_ahp, bobot_subkriteria_fahp, sum_subkriteria_ahp, sum_subkriteria_fahp, derajat_probabilitas_sub, hasil, laporan_hasil, laporan_hasil_d, hasil_dummy1
from django.db.models import Avg, Sum, Min, F
from django.contrib.auth.decorators import login_required
from django.conf import settings
# from html2excel import ExcelParser


# Create your views here.

# def base(request):
#     return render(request, 'base.html')

@login_required(login_url=settings.LOGIN_URL)
def halamanUtama(request):
    laporanD = laporan_hasil.objects.all().order_by('-tanggal')
    paginator = Paginator(laporanD, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    count = laporan_hasil.objects.count()
    konteks = {
        'page_obj': page_obj,
        'count': count,
    }

    return render(request, 'halamanUtama.html', konteks)


@login_required(login_url=settings.LOGIN_URL)
def tampilLap(request, id):
    q_dict = request.GET
    q = q_dict.get("q")
    if q is not None and q != '':
        laporanDetailD = laporan_hasil_d.objects.filter(
            laporan_hasil_id=id).order_by('-nilai_sum')[:int(q)]
        laporanD = laporan_hasil.objects.get(id=id)
        kriteriaD = kriteria.objects.all()
        paginator = Paginator(laporanDetailD, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        laporanDetailD = laporan_hasil_d.objects.filter(
            laporan_hasil_id=id).order_by('-nilai_sum')
        laporanD = laporan_hasil.objects.get(id=id)
        kriteriaD = kriteria.objects.all()
        paginator = Paginator(laporanDetailD, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

    # laporanDetailD = laporan_hasil_d.objects.filter(
    #     laporan_hasil_id=id).order_by('-nilai_sum')
    # laporanD = laporan_hasil.objects.get(id=id)
    # kriteriaD = kriteria.objects.all()
    # paginator = Paginator(laporanDetailD, 10)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)

    konteks = {
        'page_obj': page_obj,
        'laporanD': laporanD,
        'kriteriaD': kriteriaD,
        'q': q,
    }

    return render(request, 'laporan/tampil.html', konteks)


@login_required(login_url=settings.LOGIN_URL)
def hapusLaporan(request, id):

    obj = laporan_hasil.objects.get(id=id)
    obj.delete()

    return redirect('/beranda')


@login_required(login_url=settings.LOGIN_URL)
def unduhLaporan(request, id):
    q_dict = request.GET
    q = q_dict.get("q")
    laporanDetailD = laporan_hasil_d.objects.filter(
        laporan_hasil_id=id).order_by('-nilai_sum')
    laporanD = laporan_hasil.objects.get(id=id)
    kriteriaD = kriteria.objects.all()
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Laporan.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Hasil FAHP')  # this will make a sheet named Users Data

    font_style = xlwt.XFStyle()
    font_style.font.bold = False

    ws.write_merge(0, 1, 0, 0,  'NISN')
    ws.write_merge(0, 1, 1, 1, 'Nama')

    row_num = 1
    top = 0
    bot = 0
    left = 2
    right = 4
    for i in kriteriaD:
        ws.write_merge(top, bot, left, right, i.nama_kriteria)
        left = left + 3
        right = right+3
    # ws.write_merge(0, 0, 5, 7,  'TPA')
    # ws.write_merge(0, 0, 8, 10, 'Rapor')
    ws.write_merge(0, 1, 11, 11, 'Hasil')

    row = 1
    col = 2
    for i in kriteriaD:
        ws.write(row, col, 'Huruf')
        col = col+1
        ws.write(row, col, 'Bobot')
        col = col+1
        ws.write(row, col, 'x' + str(round(i.bobot_kriteria, 5)))
        col = col+1

    if q is not None:
        rows = laporan_hasil_d.objects.all().select_related('siswa').values_list('siswa_id', 'siswa__nama_siswa', 'siswa__iq_siswa_h',
                                                                                 'nilai_sub1',  'nilai_kriteria1', 'siswa__tpa_ipa_siswa_h', 'nilai_sub2', 'nilai_kriteria2', 'siswa__tpa_ipa_siswa_h', 'nilai_sub3', 'nilai_kriteria3', 'nilai_sum').order_by('-nilai_sum').distinct()[:int(q)]
    else:
        rows = laporan_hasil_d.objects.all().select_related('siswa').values_list('siswa_id', 'siswa__nama_siswa', 'siswa__iq_siswa_h',
                                                                                 'nilai_sub1',  'nilai_kriteria1', 'siswa__tpa_ipa_siswa_h', 'nilai_sub2', 'nilai_kriteria2', 'siswa__tpa_ipa_siswa_h', 'nilai_sub3', 'nilai_kriteria3', 'nilai_sum').order_by('-nilai_sum').distinct()

    print(rows.count())

    for i in rows:
        row_num += 1
        for col_num in range(len(i)):
            ws.write(row_num, col_num, i[col_num], font_style)

    wb.save(response)
    return response

    # Sheet header, first row
    # row_num = 0

    # font_style = xlwt.XFStyle()
    # font_style.font.bold = True

    # columns = ['NISN', 'Nama', 'Huruf IQ', 'Bobot IQ', '']

    # for col_num in range(len(columns)):
    #     # at 0 row 0 column
    #     ws.write(row_num, col_num, columns[col_num], font_style)

    # # Sheet body, remaining rows
    # font_style = xlwt.XFStyle()

    # rows = laporan_hasil_d.objects.all().values_list(
    #     'username', 'first_name', 'last_name', 'email')
    # for row in rows:
    #     row_num += 1
    #     for col_num in range(len(row)):
    #         ws.write(row_num, col_num, row[col_num], font_style)

    # wb.save(response)

    # return response


@login_required(login_url=settings.LOGIN_URL)
def indexSiswa(request):
    cari_dict = request.GET
    cari = cari_dict.get("cari")
    if cari is not None:
        siswaD = siswa.objects.filter(nisn_siswa=cari)
        paginator = Paginator(siswaD, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        siswaD = siswa.objects.all().order_by('nisn_siswa')
        paginator = Paginator(siswaD, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    # konteks = {
    #     'siswaD': siswaD,
    # }
    return render(request, 'siswa/index.html', {"page_obj": page_obj})


# cara 1
# def inputSiswa(request):
#     form = dataSiswa(request.POST or None, request.FILES or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return redirect('/siswa')
#         pass

#     return render(request, 'siswaForm.html', {'form': form})
# end cara1
@login_required(login_url=settings.LOGIN_URL)
def inputSiswa(request):
    if request.method == 'POST':
        nisn = request.POST['nisn_siswa']
        nama = request.POST['nama_siswa']
        iq = request.POST['iq_siswa']
        rapor_ipa = request.POST['rapor_ipa_siswa']
        rapor_ips = request.POST['rapor_ips_siswa']
        rapor_bahasa = request.POST['rapor_bahasa_siswa']
        tpa_ipa = request.POST['tpa_ipa_siswa']
        tpa_ips = request.POST['tpa_ips_siswa']
        tpa_bahasa = request.POST['tpa_bahasa_siswa']

        if int(iq) >= 80 and int(iq) < 90:
            iq_huruf = 'LA'
        elif int(iq) < 110:
            iq_huruf = 'A'
        elif int(iq) < 120:
            iq_huruf = 'HA'
        elif int(iq) <= 130:
            iq_huruf = 'S'
        elif int(iq) > 130:
            iq_huruf = 'VS'

        if float(rapor_ipa) < 40:
            rapor_ipa_h = 'SK'
        elif float(rapor_ipa) < 60:
            rapor_ipa_h = 'K'
        elif float(rapor_ipa) < 75:
            rapor_ipa_h = 'C'
        elif float(rapor_ipa) < 85:
            rapor_ipa_h = 'B'
        elif float(rapor_ipa) >= 85:
            rapor_ipa_h = 'SB'

        if float(rapor_ips) < 40:
            rapor_ips_h = 'SK'
        elif float(rapor_ips) < 60:
            rapor_ips_h = 'K'
        elif float(rapor_ips) < 75:
            rapor_ips_h = 'C'
        elif float(rapor_ips) < 85:
            rapor_ips_h = 'B'
        elif float(rapor_ips) >= 85:
            rapor_ips_h = 'SB'

        if float(rapor_bahasa) < 40:
            rapor_bahasa_h = 'SK'
        elif float(rapor_bahasa) < 60:
            rapor_bahasa_h = 'K'
        elif float(rapor_bahasa) < 75:
            rapor_bahasa_h = 'C'
        elif float(rapor_bahasa) < 85:
            rapor_bahasa_h = 'B'
        elif float(rapor_bahasa) >= 85:
            rapor_bahasa_h = 'SB'

        if float(tpa_ipa) < 40:
            tpa_ipa_h = 'SK'
        elif float(tpa_ipa) < 60:
            tpa_ipa_h = 'K'
        elif float(tpa_ipa) < 75:
            tpa_ipa_h = 'C'
        elif float(tpa_ipa) < 85:
            tpa_ipa_h = 'B'
        elif float(tpa_ipa) >= 85:
            tpa_ipa_h = 'SB'

        if float(tpa_ips) < 40:
            tpa_ips_h = 'SK'
        elif float(tpa_ips) < 60:
            tpa_ips_h = 'K'
        elif float(tpa_ips) < 75:
            tpa_ips_h = 'C'
        elif float(tpa_ips) < 85:
            tpa_ips_h = 'B'
        elif float(tpa_ips) >= 85:
            tpa_ips_h = 'SB'

        if float(tpa_bahasa) < 40:
            tpa_bahasa_h = 'SK'
        elif float(tpa_bahasa) < 60:
            tpa_bahasa_h = 'K'
        elif float(tpa_bahasa) < 75:
            tpa_bahasa_h = 'C'
        elif float(tpa_bahasa) < 85:
            tpa_bahasa_h = 'B'
        elif float(rapor_bahasa) >= 85:
            tpa_bahasa_h = 'SB'

        if siswa.objects.filter(nisn_siswa=nisn).count() > 0:
            cek = '0'
            pesan = 'NISN tidak dapat sama'
            konteks = {
                'cek': cek,
                'pesan': pesan,
            }
            return render(request, 'siswa/form.html', konteks)
        else:

            data = siswa(nisn_siswa=nisn, nama_siswa=nama,
                         iq_siswa=iq, iq_siswa_h=iq_huruf,
                         rapor_ipa_siswa=rapor_ipa, rapor_ips_siswa=rapor_ips, rapor_bahasa_siswa=rapor_bahasa,
                         tpa_ipa_siswa=tpa_ipa, tpa_ips_siswa=tpa_ips, tpa_bahasa_siswa=tpa_bahasa,
                         rapor_ipa_siswa_h=rapor_ipa_h, rapor_ips_siswa_h=rapor_ips_h, rapor_bahasa_siswa_h=rapor_bahasa_h,
                         tpa_ipa_siswa_h=tpa_ipa_h, tpa_ips_siswa_h=tpa_ips_h, tpa_bahasa_siswa_h=tpa_bahasa_h
                         )

            data.save()
            return redirect('/siswa')

        # data = siswa(nisn_siswa=nisn, nama_siswa=nama,
        #              iq_siswa=iq, iq_siswa_h=iq_huruf,
        #              rapor_ipa_siswa=rapor_ipa, rapor_ips_siswa=rapor_ips, rapor_bahasa_siswa=rapor_bahasa,
        #              tpa_ipa_siswa=tpa_ipa, tpa_ips_siswa=tpa_ips, tpa_bahasa_siswa=tpa_bahasa,
        #              rapor_ipa_siswa_h=rapor_ipa_h, rapor_ips_siswa_h=rapor_ips_h, rapor_bahasa_siswa_h=rapor_bahasa_h,
        #              tpa_ipa_siswa_h=tpa_ipa_h, tpa_ips_siswa_h=tpa_ips_h, tpa_bahasa_siswa_h=tpa_bahasa_h
        #              )

        # data.save()
        # return redirect('/siswa')
    else:
        cek = '0'
        konteks = {
            'cek': cek,
        }
        return render(request, 'siswa/form.html', konteks)


@login_required(login_url=settings.LOGIN_URL)
def updateSiswa(request):
    if request.method == 'POST':
        nisn = request.POST['nisn_siswa']
        nama = request.POST['nama_siswa']
        iq = request.POST['iq_siswa']
        rapor_ipa = request.POST['rapor_ipa_siswa']
        rapor_ips = request.POST['rapor_ips_siswa']
        rapor_bahasa = request.POST['rapor_bahasa_siswa']
        tpa_ipa = request.POST['tpa_ipa_siswa']
        tpa_ips = request.POST['tpa_ips_siswa']
        tpa_bahasa = request.POST['tpa_bahasa_siswa']

        if int(iq) >= 80 and int(iq) < 90:
            iq_huruf = 'LA'
        elif int(iq) < 110:
            iq_huruf = 'A'
        elif int(iq) < 120:
            iq_huruf = 'HA'
        elif int(iq) <= 130:
            iq_huruf = 'S'
        elif int(iq) > 130:
            iq_huruf = 'VS'

        if float(rapor_ipa) < 40:
            rapor_ipa_h = 'SK'
        elif float(rapor_ipa) < 60:
            rapor_ipa_h = 'K'
        elif float(rapor_ipa) < 75:
            rapor_ipa_h = 'C'
        elif float(rapor_ipa) < 85:
            rapor_ipa_h = 'B'
        elif float(rapor_ipa) >= 85:
            rapor_ipa_h = 'SB'

        if float(rapor_ips) < 40:
            rapor_ips_h = 'SK'
        elif float(rapor_ips) < 60:
            rapor_ips_h = 'K'
        elif float(rapor_ips) < 75:
            rapor_ips_h = 'C'
        elif float(rapor_ips) < 85:
            rapor_ips_h = 'B'
        elif float(rapor_ips) >= 85:
            rapor_ips_h = 'SB'

        if float(rapor_bahasa) < 40:
            rapor_bahasa_h = 'SK'
        elif float(rapor_bahasa) < 60:
            rapor_bahasa_h = 'K'
        elif float(rapor_bahasa) < 75:
            rapor_bahasa_h = 'C'
        elif float(rapor_bahasa) < 85:
            rapor_bahasa_h = 'B'
        elif float(rapor_bahasa) >= 85:
            rapor_bahasa_h = 'SB'

        if float(tpa_ipa) < 40:
            tpa_ipa_h = 'SK'
        elif float(tpa_ipa) < 60:
            tpa_ipa_h = 'K'
        elif float(tpa_ipa) < 75:
            tpa_ipa_h = 'C'
        elif float(tpa_ipa) < 85:
            tpa_ipa_h = 'B'
        elif float(tpa_ipa) >= 85:
            tpa_ipa_h = 'SB'

        if float(tpa_ips) < 40:
            tpa_ips_h = 'SK'
        elif float(tpa_ips) < 60:
            tpa_ips_h = 'K'
        elif float(tpa_ips) < 75:
            tpa_ips_h = 'C'
        elif float(tpa_ips) < 85:
            tpa_ips_h = 'B'
        elif float(tpa_ips) >= 85:
            tpa_ips_h = 'SB'

        if float(tpa_bahasa) < 40:
            tpa_bahasa_h = 'SK'
        elif float(tpa_bahasa) < 60:
            tpa_bahasa_h = 'K'
        elif float(tpa_bahasa) < 75:
            tpa_bahasa_h = 'C'
        elif float(tpa_bahasa) < 85:
            tpa_bahasa_h = 'B'
        elif float(rapor_bahasa) >= 85:
            tpa_bahasa_h = 'SB'

        data = siswa(nisn_siswa=nisn, nama_siswa=nama,
                     iq_siswa=iq, iq_siswa_h=iq_huruf,
                     rapor_ipa_siswa=rapor_ipa, rapor_ips_siswa=rapor_ips, rapor_bahasa_siswa=rapor_bahasa,
                     tpa_ipa_siswa=tpa_ipa, tpa_ips_siswa=tpa_ips, tpa_bahasa_siswa=tpa_bahasa,
                     rapor_ipa_siswa_h=rapor_ipa_h, rapor_ips_siswa_h=rapor_ips_h, rapor_bahasa_siswa_h=rapor_bahasa_h,
                     tpa_ipa_siswa_h=tpa_ipa_h, tpa_ips_siswa_h=tpa_ips_h, tpa_bahasa_siswa_h=tpa_bahasa_h
                     )

        data.save()
        return redirect('/siswa')

        # data = siswa(nisn_siswa=nisn, nama_siswa=nama,
        #              iq_siswa=iq, iq_siswa_h=iq_huruf,
        #              rapor_ipa_siswa=rapor_ipa, rapor_ips_siswa=rapor_ips, rapor_bahasa_siswa=rapor_bahasa,
        #              tpa_ipa_siswa=tpa_ipa, tpa_ips_siswa=tpa_ips, tpa_bahasa_siswa=tpa_bahasa,
        #              rapor_ipa_siswa_h=rapor_ipa_h, rapor_ips_siswa_h=rapor_ips_h, rapor_bahasa_siswa_h=rapor_bahasa_h,
        #              tpa_ipa_siswa_h=tpa_ipa_h, tpa_ips_siswa_h=tpa_ips_h, tpa_bahasa_siswa_h=tpa_bahasa_h
        #              )

        # data.save()
        # return redirect('/siswa')
    else:
        cek = '0'
        konteks = {
            'cek': cek,
        }
        return render(request, 'siswa/form.html', konteks)


@login_required(login_url=settings.LOGIN_URL)
def cekSiswa(request):

    cek = '1'
    konteks = {
        'cek': cek,
    }
    return render(request, 'siswa/form.html', konteks)


@login_required(login_url=settings.LOGIN_URL)
def ubahSiswa(request, id):
    siswaD = siswa.objects.filter(nisn_siswa=id)

    konteks = {
        'siswaD': siswaD,

    }

    return render(request, 'siswa/form.html', konteks)


@login_required(login_url=settings.LOGIN_URL)
def hapusSiswa(request, id):
    obj = siswa.objects.get(nisn_siswa=id)
    obj.delete()

    return redirect('/siswa')

# def inputSiswa(request):
#     form = dataSiswa()
#     context = {'form': form}
#     html_form = render_to_string

#     return render(request, 'siswaForm.html', {'form': form})


@login_required(login_url=settings.LOGIN_URL)
def indexKriteria(request):
    if request.method == 'POST':
        id = request.POST['kode']
        nama = request.POST['nama']

        data = kriteria(
            id_kriteria=id, nama_kriteria=nama
        )
        data.save()

        if bobot_kriteria_ahp.objects.count() > 0:
            bobot_kriteria_ahp.objects.all().delete()
        if sum_kriteria_ahp.objects.count() > 0:
            sum_kriteria_ahp.objects.all().delete()
        if bobot_kriteria_fahp.objects.count() > 0:
            bobot_kriteria_fahp.objects.all().delete()
        if sum_kriteria_fahp.objects.count() > 0:
            sum_kriteria_fahp.objects.all().delete()
        if derajat_probabilitas.objects.count() > 0:
            derajat_probabilitas.objects.all().delete()

        return redirect('/kriteria')
    else:
        kriteriaD = kriteria.objects.all().order_by('id_kriteria')
        if kriteriaD.count() > 0:
            maxKode = kriteriaD.raw(
                "SELECT id_kriteria, substring(id_kriteria,2,2)::integer id FROM public.fahp_kriteria group by id_kriteria order by id desc"
            )[0]
            getK = int(maxKode.id) + 1
            kode = 'C' + str(getK)
        else:
            kode = 'C1'

        subKriteriaD = sub_kriteria.objects.all().order_by('id_subkriteria')
        if subKriteriaD.count() > 0:
            maxKode = subKriteriaD.raw(
                "SELECT id_subkriteria, substring(MAX(id_subKriteria),2,3) id FROM public.fahp_sub_kriteria group by id_subkriteria order by id_subkriteria desc"
            )[0]
            getK = int(maxKode.id) + 1
            if getK > 9:
                kodes = 'S' + str(getK)
            else:
                kodes = 'S0' + str(getK)
        else:
            kodes = 'S01'

        konteks = {
            'kriteriaD': kriteriaD,
            'subKriteriaD': subKriteriaD,
            'kode': kode,
            'kodes': kodes,
        }
        return render(request, 'kriteria/form.html', konteks)


@login_required(login_url=settings.LOGIN_URL)
def ubahKriteria(request, id):
    if request.method == 'POST':
        nama = request.POST['nama']

        obj = kriteria.objects.get(id_kriteria=id)
        obj.nama_kriteria = nama
        obj.save()

        return redirect('/kriteria')
    else:
        return redirect('/kriteria')


@login_required(login_url=settings.LOGIN_URL)
def hapusKriteria(request, id):
    obj = kriteria.objects.get(id_kriteria=id)
    obj.delete()

    if bobot_kriteria_ahp.objects.count() > 0:
        bobot_kriteria_ahp.objects.all().delete()
    if sum_kriteria_ahp.objects.count() > 0:
        sum_kriteria_ahp.objects.all().delete()
    if bobot_kriteria_fahp.objects.count() > 0:
        bobot_kriteria_fahp.objects.all().delete()
    if sum_kriteria_fahp.objects.count() > 0:
        sum_kriteria_fahp.objects.all().delete()
    if derajat_probabilitas.objects.count() > 0:
        derajat_probabilitas.objects.all().delete()

    return redirect('/kriteria')


@login_required(login_url=settings.LOGIN_URL)
def subKriteria(request):
    if request.method == 'POST':
        id = request.POST['kode']
        ids = request.POST['kodes']
        nama = request.POST['nama']

        data = sub_kriteria(
            id_subkriteria=ids, nama_subkriteria=nama, kriteria_id=id,
        )
        data.save()

        if bobot_subkriteria_ahp.objects.count() > 0:
            bobot_subkriteria_ahp.objects.all().delete()
        if sum_subkriteria_ahp.objects.count() > 0:
            sum_subkriteria_ahp.objects.all().delete()
        if bobot_subkriteria_fahp.objects.count() > 0:
            bobot_subkriteria_fahp.objects.all().delete()
        if sum_subkriteria_fahp.objects.count() > 0:
            sum_subkriteria_fahp.objects.all().delete()
        if derajat_probabilitas_sub.objects.count() > 0:
            derajat_probabilitas_sub.objects.all().delete()

        return redirect('/kriteria')
    else:
        return redirect('/kriteria')


@login_required(login_url=settings.LOGIN_URL)
def ubahSubKriteria(request, id):
    if request.method == 'POST':
        nama = request.POST['nama']

        obj = sub_kriteria.objects.get(id_subkriteria=id)
        obj.nama_subkriteria = nama
        obj.save()

        return redirect('/kriteria')
    else:
        return redirect('/kriteria')


@login_required(login_url=settings.LOGIN_URL)
def hapusSubKriteria(request, id):
    obj = sub_kriteria.objects.get(id_subkriteria=id)
    obj.delete()

    if bobot_subkriteria_ahp.objects.count() > 0:
        bobot_subkriteria_ahp.objects.all().delete()
    if sum_subkriteria_ahp.objects.count() > 0:
        sum_subkriteria_ahp.objects.all().delete()
    if bobot_subkriteria_fahp.objects.count() > 0:
        bobot_subkriteria_fahp.objects.all().delete()
    if sum_subkriteria_fahp.objects.count() > 0:
        sum_subkriteria_fahp.objects.all().delete()
    if derajat_probabilitas_sub.objects.count() > 0:
        derajat_probabilitas_sub.objects.all().delete()

    return redirect('/kriteria')


@login_required(login_url=settings.LOGIN_URL)
def pembobotanKriteria(request):
    if request.method == 'POST':

        # Insert data bobot kriteria ahp
        for datak in kriteria.objects.all():
            for datak2 in kriteria.objects.all():
                k1 = request.POST['k1'+datak.id_kriteria+datak2.id_kriteria]
                nk1 = request.POST['nk1'+datak.id_kriteria+datak2.id_kriteria]
                k2 = request.POST['k2'+datak.id_kriteria+datak2.id_kriteria]
                nk2 = request.POST['nk2'+datak.id_kriteria+datak2.id_kriteria]
                bobot = (float(nk1)/float(nk2))
                data = bobot_kriteria_ahp(
                    id=k1+k2, kriteria1_id=k1, kriteria2=k2, bobotk1=nk1, bobotk2=nk2, bobot_normal=bobot
                )
                data.save()

        # insert data kriteria fahp
        skala_fuzzyn1 = skala_fuzzy(id='1', l='1', m='1', u='1')
        skala_fuzzyn2 = skala_fuzzy(id='2', l='1', m='2', u='3')
        skala_fuzzyn3 = skala_fuzzy(id='3', l='2', m='3', u='4')
        skala_fuzzyn4 = skala_fuzzy(id='4', l='3', m='4', u='5')
        skala_fuzzyn5 = skala_fuzzy(id='5', l='4', m='5', u='6')
        skala_fuzzyn6 = skala_fuzzy(id='6', l='5', m='6', u='7')
        skala_fuzzyn7 = skala_fuzzy(id='7', l='6', m='7', u='8')
        skala_fuzzyn8 = skala_fuzzy(id='8', l='7', m='8', u='9')
        skala_fuzzyn9 = skala_fuzzy(id='9', l='9', m='9', u='9')

        skala_list = [skala_fuzzyn1, skala_fuzzyn2, skala_fuzzyn3, skala_fuzzyn4,
                      skala_fuzzyn5, skala_fuzzyn6, skala_fuzzyn7, skala_fuzzyn8, skala_fuzzyn9]

        for i in skala_list:
            i.save()

        skala_fuzzy1r = skala_fuzzy2(id='1', l='1', m='1', u='1')
        skala_fuzzy2r = skala_fuzzy2(id='2', l='3', m='2', u='1')
        skala_fuzzy3r = skala_fuzzy2(id='3', l='4', m='3', u='2')
        skala_fuzzy4r = skala_fuzzy2(id='4', l='5', m='4', u='3')
        skala_fuzzy5r = skala_fuzzy2(id='5', l='6', m='5', u='4')
        skala_fuzzy6r = skala_fuzzy2(id='6', l='7', m='6', u='5')
        skala_fuzzy7r = skala_fuzzy2(id='7', l='8', m='7', u='6')
        skala_fuzzy8r = skala_fuzzy2(id='8', l='9', m='8', u='7')
        skala_fuzzy9r = skala_fuzzy2(id='9', l='9', m='9', u='9')

        skala_list2 = [skala_fuzzy1r, skala_fuzzy2r, skala_fuzzy3r, skala_fuzzy4r,
                       skala_fuzzy5r, skala_fuzzy6r, skala_fuzzy7r, skala_fuzzy8r, skala_fuzzy9r]

        for i in skala_list2:
            i.save()

        for datak in kriteria.objects.all():
            for datak2 in kriteria.objects.all():
                k1 = request.POST['k1'+datak.id_kriteria+datak2.id_kriteria]
                nk1 = request.POST['nk1'+datak.id_kriteria+datak2.id_kriteria]
                k2 = request.POST['k2'+datak.id_kriteria+datak2.id_kriteria]
                nk2 = request.POST['nk2'+datak.id_kriteria+datak2.id_kriteria]
                # print(round(float(nk2)))
                data = bobot_kriteria_fahp(
                    id=k1+k2, kriteria1_id=k1, kriteria2=k2, bobotk1_id=round(float(nk1)), bobotk2_id=round(float(nk2))
                )
                data.save()

        return redirect('/fahp/kriteria')
    # End Insert data bobot kriteria fahp

    else:
        # data = kriteria.objects.all()
        # datab = bobot_kriteria_ahp.objects.all()
        # konteks = {
        #     'data': data,
        #     'datab': datab,
        # }

        # TES

        if bobot_kriteria_ahp.objects.count() > 0:

            # Insert sum_kriteria_ahp
            sums = bobot_kriteria_ahp.objects.raw(
                "SELECT 1 id, kriteria2, sum(bobot_normal) bobot_normal FROM public.fahp_bobot_kriteria_ahp group by kriteria2 order by kriteria2")
            for jumlah in sums:
                id = 'n'+jumlah.kriteria2
                kriteria_id = jumlah.kriteria2
                sum_ahp = jumlah.bobot_normal

                data1 = sum_kriteria_ahp(
                    id=id, kriteria_id=kriteria_id, sum_ahp=sum_ahp
                )
                data1.save()
        # End Insert sum_kriteria_ahp

        # Update nilai normalisasi pada tabel bobot_kriteria_ahp
            for norm in bobot_kriteria_ahp.objects.all():
                for sums in sum_kriteria_ahp.objects.all():
                    if sums.kriteria_id == norm.kriteria2:
                        normalisasi = norm.bobot_normal/sums.sum_ahp
                        obj = bobot_kriteria_ahp.objects.get(id=norm.id)
                        obj.nilai_norm = normalisasi
                        obj.save()
        # Update nilai normalisasi pada tabel bobot_kriteria_ahp

        # Update nilai bobot ahp sum_kriteria_ahp
            sums2 = bobot_kriteria_ahp.objects.raw(
                "SELECT 1 id, avg(nilai_norm)::numeric avg_normalisasi, kriteria1_id FROM public.fahp_bobot_kriteria_ahp group by kriteria1_id"
            )

            for jum in sums2:
                id = 'n'+jum.kriteria1_id
                kriteria_id = jum.kriteria1_id
                bobot_ahp = jum.avg_normalisasi

                # print(jum.avg_normalisasi)
                obj = sum_kriteria_ahp.objects.get(id=id)
                obj.bobot_ahp = bobot_ahp
                obj.save()
        # End update sum_kriteria_ahp

        # Update nilai normalisasi pada tabel bobot_kriteria_ahp
            for norm in bobot_kriteria_ahp.objects.all():
                for sums in sum_kriteria_ahp.objects.all():
                    if sums.kriteria_id == norm.kriteria2:
                        konsistensi = norm.bobot_normal*sums.bobot_ahp
                        # print(str(norm.bobot_normal)+'||'+str(sums.bobot_ahp))
                        obj = bobot_kriteria_ahp.objects.get(id=norm.id)
                        obj.nilai_konsistensi = konsistensi
                        obj.save()
        # Update nilai normalisasi pada tabel bobot_kriteria_ahp

        # Update sum nilai_konsistensi, table sum_kriteria_ahp
            sums2 = bobot_kriteria_ahp.objects.raw(
                "SELECT 1 id, sum(nilai_konsistensi)::numeric sum_kosistensi, kriteria1_id FROM public.fahp_bobot_kriteria_ahp group by kriteria1_id order by kriteria1_id"
            )
            datas = sum_kriteria_ahp.objects.all()

            for jum in sums2:
                id = 'n'+jum.kriteria1_id
                kriteria_id = jum.kriteria1_id
                sum_kosistensi = jum.sum_kosistensi

                for sumary in datas:
                    # print(jum.avg_normalisasi)
                    if sumary.kriteria_id == jum.kriteria1_id:
                        obj = sum_kriteria_ahp.objects.get(id=id)
                        obj.sum_kosistensi = sum_kosistensi
                        obj.sum_kosistensi2 = float(
                            sum_kosistensi)/sumary.bobot_ahp
                        obj.save()
        # End update  Update sum nilai_konsistensi, table sum_kriteria_ahp

        # Select Data
            data = kriteria.objects.all().order_by('id_kriteria')
            datab = bobot_kriteria_ahp.objects.raw(
                "SELECT id, kriteria1_id, bobotk1, kriteria2, bobotk2, ROUND(bobot_normal::numeric, 2) bobot_normal, round(nilai_norm::numeric,2) normalisasi FROM public.fahp_bobot_kriteria_ahp order by kriteria1_id")
            sum = bobot_kriteria_ahp.objects.raw(
                "SELECT 1 id, kriteria2, round(sum(bobot_normal)::numeric,2) bobot_normal FROM public.fahp_bobot_kriteria_ahp group by kriteria2 order by kriteria2")

            sum2 = bobot_kriteria_ahp.objects.raw(
                "SELECT 1 id, kriteria2, round(sum(nilai_norm)::numeric,2) sum_normalisasi FROM public.fahp_bobot_kriteria_ahp group by kriteria2 order by kriteria2")
            dataz = sum_kriteria_ahp.objects.all().order_by('kriteria_id')
            # dataz = sum_kriteria_ahp.objects.annotate(
            #     bobot_ahp=round('bobot_ahp', 2))
            avg = sum_kriteria_ahp.objects.aggregate(
                avg=Avg("sum_kosistensi2"))
            count = sum_kriteria_ahp.objects.count()
            ci = (avg['avg']-count)/(count-1)

            if count == 1:
                cr = ci/0
            elif count == 2:
                cr = ci/0
            elif count == 3:
                cr = ci/0.58
            elif count == 4:
                cr = ci/0.90
            elif count == 5:
                cr = ci/1.12
            elif count == 6:
                cr = ci/1.24
            elif count == 7:
                cr = ci/1.32
            elif count == 8:
                cr = ci/1.41
            elif count == 9:
                cr = ci/1.45
            elif count == 10:
                cr = ci/1.49

            if cr < 0.10:
                result = 'Matrix konsisten'
                r = 1
            else:
                result = 'Matrix tidak konsisten'
                r = 0

            konteks = {
                'data': data,
                'datab': datab,
                'dataz': dataz,
                'sum': sum,
                'sum2': sum2,
                'avg': avg,
                'ci': ci,
                'cr': cr,
                'result': result,
                'r': r,
            }

            return render(request, 'bobot/detail.html', konteks)
        #  EndTes
        else:
            data = kriteria.objects.all().order_by('id_kriteria')
            datab = bobot_kriteria_ahp.objects.all()
            # datab = None
            konteks = {
                'data': data,
                'datab': datab,
            }
            return render(request, 'bobot/form.html', konteks)


@login_required(login_url=settings.LOGIN_URL)
def bersihKriteria(request):
    bobot_kriteria_ahp.objects.all().delete()

    return redirect('/fahp/kriteria/')


@login_required(login_url=settings.LOGIN_URL)
def fahpKriteria(request):

    sums = bobot_kriteria_fahp.objects.raw(
        "SELECT 1 id, kriteria1_id, sum(sk1.l/sk2.l) sum_l,  sum(sk1.m/sk2.m) sum_m, sum(sk1.u/sk2.u) sum_u FROM public.fahp_bobot_kriteria_fahp b JOIN public.fahp_skala_fuzzy sk1 ON b.bobotk1_id=sk1.id join public.fahp_skala_fuzzy2 sk2 ON b.bobotk2_id=sk2.id group by kriteria1_id order by kriteria1_id")
    for jumlah in sums:
        id = 'f'+jumlah.kriteria1_id
        kriteria_id = jumlah.kriteria1_id
        sum_l = jumlah.sum_l
        sum_m = jumlah.sum_m
        sum_u = jumlah.sum_u

        data = sum_kriteria_fahp(
            id=id, kriteria_id=kriteria_id, jumlah_l=sum_l, jumlah_m=sum_m, jumlah_u=sum_u,
        )
        data.save()

    sum_l = sum_kriteria_fahp.objects.aggregate(sum=Sum('jumlah_l'))
    sum_m = sum_kriteria_fahp.objects.aggregate(sum=Sum('jumlah_m'))
    sum_u = sum_kriteria_fahp.objects.aggregate(sum=Sum('jumlah_u'))

    sums_fahp = sum_kriteria_fahp.objects.all()
    for jum in sums_fahp:
        id = jum.id
        si_l = jum.jumlah_l/sum_u['sum']
        si_m = jum.jumlah_m/sum_m['sum']
        si_u = jum.jumlah_u/sum_l['sum']

        # print(jum.avg_normalisasi)
        obj = sum_kriteria_fahp.objects.get(id=id)
        obj.si_l = si_l
        obj.si_m = si_m
        obj.si_u = si_u
        obj.save()

    # Probabilitas i >= j

    for i in sum_kriteria_fahp.objects.all():
        for j in sum_kriteria_fahp.objects.all():
            if j.id != i.id:
                if i.si_m >= j.si_m:
                    id = i.kriteria_id + j.kriteria_id
                    kriteria_id = i.kriteria_id
                    kriteria1 = i.kriteria.nama_kriteria
                    kriteria2 = j.kriteria.nama_kriteria
                    prob = 1

                    data = derajat_probabilitas(
                        id=id, kriteria_id=kriteria_id, nilai=prob, kriteria1=kriteria1, kriteria2=kriteria2,
                    )
                    data.save()

                elif j.si_l >= i.si_u:
                    id = i.kriteria_id + j.kriteria_id
                    kriteria_id = i.kriteria_id
                    kriteria1 = i.kriteria.nama_kriteria
                    kriteria2 = j.kriteria.nama_kriteria
                    prob = 0
                    data = derajat_probabilitas(
                        id=id, kriteria_id=kriteria_id, nilai=prob, kriteria1=kriteria1, kriteria2=kriteria2,
                    )
                    data.save()
                else:
                    id = i.kriteria_id + j.kriteria_id
                    kriteria_id = i.kriteria_id
                    kriteria1 = i.kriteria.nama_kriteria
                    kriteria2 = j.kriteria.nama_kriteria
                    prob = (j.si_l - i.si_u) / \
                        ((i.si_m - i.si_u)-(j.si_m-j.si_l))

                    data = derajat_probabilitas(
                        id=id, kriteria_id=kriteria_id, nilai=prob, kriteria1=kriteria1, kriteria2=kriteria2,
                    )
                    data.save()

    # Select Data

    sum_fahp = sum_kriteria_fahp.objects.all()
    bfahp = bobot_kriteria_fahp.objects.all()

    min = derajat_probabilitas.objects.values('kriteria1', 'kriteria_id').annotate(
        min=Min('nilai')).order_by('kriteria_id')

    jumlah = 0.0
    for i in min:
        jumlah = jumlah + i['min']

    probabilitas = derajat_probabilitas.objects.all()

    for hasil in min:
        id_kriteria = hasil['kriteria_id']
        obj = kriteria.objects.get(id_kriteria=id_kriteria)
        obj.bobot_kriteria = hasil['min']/jumlah
        obj.save()

    kfahp = kriteria.objects.all()

    # print(jumlah)

    konteks = {
        'kfahp': kfahp,
        'bfahp': bfahp,
        'sum_fahp': sum_fahp,
        'probabilitas': probabilitas,
        'min': min

    }

    return render(request, 'bobot/fahpKriteria.html', konteks)


@login_required(login_url=settings.LOGIN_URL)
def subKriteriaPilih(request):
    # if bobot_subkriteria_ahp.objects.count() > 0:
    #     return render(request, 'bobotSub/form.html')

    # else:

    if request.method == 'POST':
        id = request.POST['kriteria']
        data = sub_kriteria.objects.filter(kriteria_id=id)
        datak = kriteria.objects.all().order_by('id_kriteria')
        # krit = kriteria.objects.filter(kriteria_id=id)

        if data.count() > 0:

            # konteks = {
            #     'data': data,
            #     'datak': datak,
            #     'krit': krit,
            # }
            return redirect('pembobotanSubKriteria', id)
        else:
            konteks = {
                'datak': datak,
            }
            return render(request, 'bobotSub/kosong.html', konteks)

    else:

        datak = kriteria.objects.all().order_by('id_kriteria')
        konteks = {
            'datak': datak,
        }
        return render(request, 'bobotSub/index.html', konteks)


@login_required(login_url=settings.LOGIN_URL)
def pembobotanSubKriteria(request, id_k):
    if request.method == 'POST':

        # Insert data bobot sub kriteria ahp
        for datak in sub_kriteria.objects.filter(kriteria_id=id_k):
            for datak2 in sub_kriteria.objects.filter(kriteria_id=id_k):
                k1 = request.POST['k1' +
                                  datak.id_subkriteria+datak2.id_subkriteria]
                nk1 = request.POST['nk1' +
                                   datak.id_subkriteria+datak2.id_subkriteria]
                k2 = request.POST['k2' +
                                  datak.id_subkriteria+datak2.id_subkriteria]
                nk2 = request.POST['nk2' +
                                   datak.id_subkriteria+datak2.id_subkriteria]
                bobot = (float(nk1)/float(nk2))
                # print('tes')
                data = bobot_subkriteria_ahp(
                    id=k1+k2, subkriteria1_id=k1, subkriteria2=k2, bobotk1=nk1, bobotk2=nk2, bobot_normal=bobot, kriteria_id=id_k,
                )
                data.save()

        # insert data kriteria fahp
        skala_fuzzyn1 = skala_fuzzy(id='1', l='1', m='1', u='1')
        skala_fuzzyn2 = skala_fuzzy(id='2', l='1', m='2', u='3')
        skala_fuzzyn3 = skala_fuzzy(id='3', l='2', m='3', u='4')
        skala_fuzzyn4 = skala_fuzzy(id='4', l='3', m='4', u='5')
        skala_fuzzyn5 = skala_fuzzy(id='5', l='4', m='5', u='6')
        skala_fuzzyn6 = skala_fuzzy(id='6', l='5', m='6', u='7')
        skala_fuzzyn7 = skala_fuzzy(id='7', l='6', m='7', u='8')
        skala_fuzzyn8 = skala_fuzzy(id='8', l='7', m='8', u='9')
        skala_fuzzyn9 = skala_fuzzy(id='9', l='9', m='9', u='9')

        skala_list = [skala_fuzzyn1, skala_fuzzyn2, skala_fuzzyn3, skala_fuzzyn4,
                      skala_fuzzyn5, skala_fuzzyn6, skala_fuzzyn7, skala_fuzzyn8, skala_fuzzyn9]

        for i in skala_list:
            i.save()

        skala_fuzzy1r = skala_fuzzy2(id='1', l='1', m='1', u='1')
        skala_fuzzy2r = skala_fuzzy2(id='2', l='3', m='2', u='1')
        skala_fuzzy3r = skala_fuzzy2(id='3', l='4', m='3', u='2')
        skala_fuzzy4r = skala_fuzzy2(id='4', l='5', m='4', u='3')
        skala_fuzzy5r = skala_fuzzy2(id='5', l='6', m='5', u='4')
        skala_fuzzy6r = skala_fuzzy2(id='6', l='7', m='6', u='5')
        skala_fuzzy7r = skala_fuzzy2(id='7', l='8', m='7', u='6')
        skala_fuzzy8r = skala_fuzzy2(id='8', l='9', m='8', u='7')
        skala_fuzzy9r = skala_fuzzy2(id='9', l='9', m='9', u='9')

        skala_list2 = [skala_fuzzy1r, skala_fuzzy2r, skala_fuzzy3r, skala_fuzzy4r,
                       skala_fuzzy5r, skala_fuzzy6r, skala_fuzzy7r, skala_fuzzy8r, skala_fuzzy9r]

        for i in skala_list2:
            i.save()

        for datak in sub_kriteria.objects.filter(kriteria_id=id_k):
            for datak2 in sub_kriteria.objects.filter(kriteria_id=id_k):
                k1 = request.POST['k1' +
                                  datak.id_subkriteria+datak2.id_subkriteria]
                nk1 = request.POST['nk1' +
                                   datak.id_subkriteria+datak2.id_subkriteria]
                k2 = request.POST['k2' +
                                  datak.id_subkriteria+datak2.id_subkriteria]
                nk2 = request.POST['nk2' +
                                   datak.id_subkriteria+datak2.id_subkriteria]
                # print(round(float(nk2)))
                data = bobot_subkriteria_fahp(
                    id=k1+k2, subkriteria1_id=k1, subkriteria2=k2, bobotk1_id=round(float(nk1)), bobotk2_id=round(float(nk2)),  kriteria_id=id_k,
                )
                data.save()

        return redirect('pembobotanSubKriteria', id_k)
    # End Insert data bobot kriteria fahp

    else:
        # data = kriteria.objects.all()
        # datab = bobot_kriteria_ahp.objects.all()
        # konteks = {
        #     'data': data,
        #     'datab': datab,
        # }

        # TES

        if bobot_subkriteria_ahp.objects.filter(kriteria_id=id_k).count() > 0:

            # Insert sum_kriteria_ahp
            sums = bobot_subkriteria_ahp.objects.raw(
                "SELECT 1 id, subkriteria2, kriteria_id, sum(bobot_normal) bobot_normal FROM public.fahp_bobot_subkriteria_ahp where kriteria_id ='"+id_k+"' group by subkriteria2, kriteria_id order by subkriteria2")
            for jumlah in sums:
                id = 'n'+jumlah.subkriteria2
                subkriteria_id = jumlah.subkriteria2
                sum_ahp = jumlah.bobot_normal
                id_krit = jumlah.kriteria_id

                data1 = sum_subkriteria_ahp(
                    id=id, subkriteria_id=subkriteria_id, sum_ahp=sum_ahp, kriteria_id=id_krit,
                )
                data1.save()
        # End Insert sum_kriteria_ahp

        # Update nilai normalisasi pada tabel bobot_kriteria_ahp
            for norm in bobot_subkriteria_ahp.objects.all():
                for sums in sum_subkriteria_ahp.objects.all():
                    if sums.subkriteria_id == norm.subkriteria2:
                        normalisasi = norm.bobot_normal/sums.sum_ahp
                        obj = bobot_subkriteria_ahp.objects.get(id=norm.id)
                        obj.nilai_norm = normalisasi
                        obj.save()
        # Update nilai normalisasi pada tabel bobot_kriteria_ahp

        # Update nilai bobot ahp sum_kriteria_ahp
            sums2 = bobot_subkriteria_ahp.objects.raw(
                "SELECT 1 id, avg(nilai_norm)::numeric avg_normalisasi, subkriteria1_id FROM public.fahp_bobot_subkriteria_ahp group by subkriteria1_id"
            )

            for jum in sums2:
                id = 'n'+jum.subkriteria1_id
                subkriteria_id = jum.subkriteria1_id
                bobot_ahp = jum.avg_normalisasi

                # print(jum.avg_normalisasi)
                obj = sum_subkriteria_ahp.objects.get(id=id)
                obj.bobot_ahp = bobot_ahp
                obj.save()
        # End update sum_kriteria_ahp

        # Update nilai normalisasi pada tabel bobot_kriteria_ahp
            for norm in bobot_subkriteria_ahp.objects.all():
                for sums in sum_subkriteria_ahp.objects.all():
                    if sums.subkriteria_id == norm.subkriteria2:
                        konsistensi = norm.bobot_normal*sums.bobot_ahp
                        # print(str(norm.bobot_normal)+'||'+str(sums.bobot_ahp))
                        obj = bobot_subkriteria_ahp.objects.get(id=norm.id)
                        obj.nilai_konsistensi = konsistensi
                        obj.save()
        # Update nilai normalisasi pada tabel bobot_kriteria_ahp

        # Update sum nilai_konsistensi, table sum_kriteria_ahp
            sums2 = bobot_subkriteria_ahp.objects.raw(
                "SELECT 1 id, sum(nilai_konsistensi)::numeric sum_kosistensi, subkriteria1_id FROM public.fahp_bobot_subkriteria_ahp group by subkriteria1_id order by subkriteria1_id"
            )
            datas = sum_subkriteria_ahp.objects.all()

            for jum in sums2:
                id = 'n'+jum.subkriteria1_id
                subkriteria_id = jum.subkriteria1_id
                sum_kosistensi = jum.sum_kosistensi

                for sumary in datas:
                    # print(jum.avg_normalisasi)
                    if sumary.subkriteria_id == jum.subkriteria1_id:
                        obj = sum_subkriteria_ahp.objects.get(id=id)
                        obj.sum_kosistensi = sum_kosistensi
                        obj.sum_kosistensi2 = float(
                            sum_kosistensi)/sumary.bobot_ahp
                        obj.save()
        # End update  Update sum nilai_konsistensi, table sum_kriteria_ahp

        # Select Data
            data = sub_kriteria.objects.filter(kriteria_id=id_k)
            datab = bobot_subkriteria_ahp.objects.raw(
                "SELECT id, subkriteria1_id, bobotk1, subkriteria2, bobotk2, ROUND(bobot_normal::numeric, 2) bobot_normal, round(nilai_norm::numeric,2) normalisasi FROM public.fahp_bobot_subkriteria_ahp")
            sum = bobot_subkriteria_ahp.objects.raw(
                "SELECT 1 id, subkriteria2, round(sum(bobot_normal)::numeric,2) bobot_normal FROM public.fahp_bobot_subkriteria_ahp where kriteria_id ='"+id_k+"' group by subkriteria2 order by subkriteria2")

            sum2 = bobot_subkriteria_ahp.objects.raw(
                "SELECT 1 id, subkriteria2, round(sum(nilai_norm)::numeric,2) sum_normalisasi FROM public.fahp_bobot_subkriteria_ahp where kriteria_id ='"+id_k+"' group by subkriteria2 order by subkriteria2")
            dataz = sum_subkriteria_ahp.objects.filter(
                kriteria_id=id_k).order_by('subkriteria_id')

            krit = kriteria.objects.get(id_kriteria=id_k)
            # dataz = sum_kriteria_ahp.objects.annotate(
            #     bobot_ahp=round('bobot_ahp', 2))
            avg = sum_subkriteria_ahp.objects.filter(kriteria_id=id_k).aggregate(
                avg=Avg("sum_kosistensi2"))
            count = sum_subkriteria_ahp.objects.filter(
                kriteria_id=id_k).count()
            ci = (avg['avg']-count)/(count-1)

            if count == 1:
                cr = ci/0
            elif count == 2:
                cr = ci/0
            elif count == 3:
                cr = ci/0.58
            elif count == 4:
                cr = ci/0.90
            elif count == 5:
                cr = ci/1.12
            elif count == 6:
                cr = ci/1.24
            elif count == 7:
                cr = ci/1.32
            elif count == 8:
                cr = ci/1.41
            elif count == 9:
                cr = ci/1.45
            elif count == 10:
                cr = ci/1.49

            if cr < 0.10:
                result = 'Matrix konsisten'
                r = 1
            else:
                result = 'Matrix tidak konsisten'
                r = 0

            konteks = {
                'data': data,
                'datab': datab,
                'dataz': dataz,
                'sum': sum,
                'sum2': sum2,
                'avg': avg,
                'ci': ci,
                'cr': cr,
                'result': result,
                'r': r,
                'krit': krit,
            }

            return render(request, 'bobotSub/detail.html', konteks)
        #  EndTes
        else:

            data = sub_kriteria.objects.filter(kriteria_id=id_k)

            # datak = kriteria.objects.all().order_by('id_kriteria')
            krit = kriteria.objects.get(id_kriteria=id_k)
            # data = sub_kriteria.objects.all()
            # print(krit)
            # datab = bobot_kriteria_ahp.objects.all()
            datab = None
            konteks = {
                'data': data,
                'datab': datab,
                'krit': krit,
            }
            return render(request, 'bobotSub/form.html', konteks)


@login_required(login_url=settings.LOGIN_URL)
def bersihSubKriteria(request, id_k):
    obj = bobot_subkriteria_ahp.objects.filter(kriteria_id=id_k)
    obj.delete()

    return redirect('/fahp/subkriteria/')


@login_required(login_url=settings.LOGIN_URL)
def fahpSubKriteria(request, id_k):

    sums = bobot_subkriteria_fahp.objects.raw(
        "SELECT 1 id, subkriteria1_id, kriteria_id, sum(sk1.l/sk2.l) sum_l,  sum(sk1.m/sk2.m) sum_m, sum(sk1.u/sk2.u) sum_u FROM public.fahp_bobot_subkriteria_fahp b JOIN public.fahp_skala_fuzzy sk1 ON b.bobotk1_id=sk1.id join public.fahp_skala_fuzzy2 sk2 ON b.bobotk2_id=sk2.id where kriteria_id = '"+id_k+"' group by subkriteria1_id, kriteria_id order by subkriteria1_id")
    for jumlah in sums:
        id = 'f'+jumlah.subkriteria1_id
        subkriteria_id = jumlah.subkriteria1_id
        kriteria_id = jumlah.kriteria_id
        sum_l = jumlah.sum_l
        sum_m = jumlah.sum_m
        sum_u = jumlah.sum_u

        data = sum_subkriteria_fahp(
            id=id, subkriteria_id=subkriteria_id, jumlah_l=sum_l, jumlah_m=sum_m, jumlah_u=sum_u, kriteria_id=kriteria_id
        )
        data.save()

    sum_l = sum_subkriteria_fahp.objects.filter(
        kriteria_id=id_k).aggregate(sum=Sum('jumlah_l'))
    sum_m = sum_subkriteria_fahp.objects.filter(
        kriteria_id=id_k).aggregate(sum=Sum('jumlah_m'))
    sum_u = sum_subkriteria_fahp.objects.filter(
        kriteria_id=id_k).aggregate(sum=Sum('jumlah_u'))

    sums_fahp = sum_subkriteria_fahp.objects.all()
    for jum in sums_fahp:
        id = jum.id
        si_l = jum.jumlah_l/sum_u['sum']
        si_m = jum.jumlah_m/sum_m['sum']
        si_u = jum.jumlah_u/sum_l['sum']

        # print(jum.avg_normalisasi)
        obj = sum_subkriteria_fahp.objects.get(id=id)
        obj.si_l = si_l
        obj.si_m = si_m
        obj.si_u = si_u
        obj.save()

    # Probabilitas i >= j

    for i in sum_subkriteria_fahp.objects.filter(kriteria_id=id_k):
        for j in sum_subkriteria_fahp.objects.filter(kriteria_id=id_k):
            if j.id != i.id:
                if i.si_m >= j.si_m:
                    id = i.subkriteria_id + j.subkriteria_id
                    subkriteria_id = i.subkriteria_id
                    kriteria_id = i.kriteria_id
                    subkriteria1 = i.subkriteria.nama_subkriteria
                    subkriteria2 = j.subkriteria.nama_subkriteria
                    prob = 1

                    data = derajat_probabilitas_sub(
                        id=id, subkriteria_id=subkriteria_id, nilai=prob, subkriteria1=subkriteria1, subkriteria2=subkriteria2, kriteria_id=kriteria_id
                    )
                    data.save()

                elif j.si_l >= i.si_u:
                    id = i.subkriteria_id + j.subkriteria_id
                    subkriteria_id = i.subkriteria_id
                    kriteria_id = i.kriteria_id
                    subkriteria1 = i.subkriteria.nama_subkriteria
                    subkriteria2 = j.subkriteria.nama_subkriteria
                    prob = 0
                    data = derajat_probabilitas_sub(
                        id=id, subkriteria_id=subkriteria_id, nilai=prob, subkriteria1=subkriteria1, subkriteria2=subkriteria2, kriteria_id=kriteria_id
                    )
                    data.save()
                else:
                    id = i.subkriteria_id + j.subkriteria_id
                    subkriteria_id = i.subkriteria_id
                    kriteria_id = i.kriteria_id
                    subkriteria1 = i.subkriteria.nama_subkriteria
                    subkriteria2 = j.subkriteria.nama_subkriteria
                    prob = (j.si_l - i.si_u) / \
                        ((i.si_m - i.si_u)-(j.si_m-j.si_l))

                    data = derajat_probabilitas_sub(
                        id=id, subkriteria_id=subkriteria_id, nilai=prob, subkriteria1=subkriteria1, subkriteria2=subkriteria2, kriteria_id=kriteria_id
                    )
                    data.save()

    # Select Data

    sum_fahp = sum_subkriteria_fahp.objects.filter(kriteria_id=id_k)
    bfahp = bobot_subkriteria_fahp.objects.filter(kriteria_id=id_k)

    min = derajat_probabilitas_sub.objects.filter(kriteria_id=id_k).values('subkriteria1', 'subkriteria_id').annotate(
        min=Min('nilai')).order_by('subkriteria_id')

    jumlah = 0.0
    for i in min:
        jumlah = jumlah + i['min']

    probabilitas = derajat_probabilitas_sub.objects.filter(kriteria_id=id_k)

    for hasil in min:
        id_subkriteria = hasil['subkriteria_id']
        obj = sub_kriteria.objects.get(id_subkriteria=id_subkriteria)
        obj.bobot_subkriteria = hasil['min']/jumlah
        obj.save()

    kfahp = sub_kriteria.objects.all().filter(kriteria_id=id_k)

    # print(jumlah)

    konteks = {
        'kfahp': kfahp,
        'bfahp': bfahp,
        'sum_fahp': sum_fahp,
        'probabilitas': probabilitas,
        'min': min

    }

    return render(request, 'bobotSub/fahp.html', konteks)


@login_required(login_url=settings.LOGIN_URL)
def indexHasil(request):
    siswaD = siswa.objects.all()
    kriteriaD = kriteria.objects.all()
    subD = sub_kriteria.objects.all()

    for dataSiswa in siswaD:
        for dataKriteria in kriteriaD:
            for dataSub in subD:
                if dataKriteria.id_kriteria == dataSub.kriteria_id:
                    if dataSiswa.iq_siswa_h == dataSub.nama_subkriteria and dataSub.kriteria_id == 'C1':
                        id = dataSiswa.nisn_siswa+dataKriteria.id_kriteria
                        idSiswa = dataSiswa.nisn_siswa
                        idKriteria = dataKriteria.id_kriteria
                        idSub = dataSub.id_subkriteria
                        nilai_sub = dataSub.bobot_subkriteria
                        nilai_kriteria = dataKriteria.bobot_kriteria
                        # print(dataSub.kriteria_id + '|' +
                        #       str(dataSub.id_subkriteria)+'|'+dataSub.nama_subkriteria+'|'+dataSiswa.iq_siswa_h+'|'+id)

                        obj = hasil(
                            id=id, siswa_id=idSiswa, kriteria_id=idKriteria, subkriteria_id=idSub, nilai_sub=nilai_sub, nilai_kriteria=nilai_kriteria,
                        )
                        obj.save()
                    elif dataSiswa.rapor_ipa_siswa_h == dataSub.nama_subkriteria and dataSub.kriteria_id == 'C3':
                        id = dataSiswa.nisn_siswa+dataKriteria.id_kriteria
                        idSiswa = dataSiswa.nisn_siswa
                        idKriteria = dataKriteria.id_kriteria
                        idSub = dataSub.id_subkriteria
                        nilai_sub = dataSub.bobot_subkriteria
                        nilai_kriteria = dataKriteria.bobot_kriteria
                        # print(nilai_sub)

                        obj = hasil(
                            id=id, siswa_id=idSiswa, kriteria_id=idKriteria, subkriteria_id=idSub, nilai_sub=nilai_sub, nilai_kriteria=nilai_kriteria,
                        )
                        obj.save()
                    elif dataSiswa.tpa_ipa_siswa_h == dataSub.nama_subkriteria and dataSub.kriteria_id == 'C2':
                        id = dataSiswa.nisn_siswa+dataKriteria.id_kriteria
                        idSiswa = dataSiswa.nisn_siswa
                        idKriteria = dataKriteria.id_kriteria
                        idSub = dataSub.id_subkriteria
                        nilai_sub = dataSub.bobot_subkriteria
                        nilai_kriteria = dataKriteria.bobot_kriteria
                        # print(dataSub.kriteria_id + '|' +
                        #       str(dataSub.bobot_subkriteria)+'|'+dataSub.nama_subkriteria+'|'+dataSiswa.tpa_ipa_siswa_h+'|'+id)

                        obj = hasil(
                            id=id, siswa_id=idSiswa, kriteria_id=idKriteria, subkriteria_id=idSub, nilai_sub=nilai_sub, nilai_kriteria=nilai_kriteria,
                        )
                        obj.save()

    sum = hasil.objects.values('siswa_id').annotate(
        sum=Sum(F('nilai_sub')*F('nilai_kriteria'))).order_by('-sum')
    kali = hasil.objects.all().annotate(
        kali=F('nilai_sub')*F('nilai_kriteria'))

    # print(sum)
    # for x in sum:
    #     print(str(x.siswa_id)+'|'+str(x.sum))

    hasilD = hasil.objects.all()

    kode = laporan_hasil.objects.all().order_by('id')
    if kode.count() > 0:
        maxKode = laporan_hasil.objects.raw(
            "SELECT id, substring(MAX(id),2,3) ids FROM public.fahp_laporan_hasil group by id order by id desc"
        )[0]
        getK = int(maxKode.ids) + 1
        if getK > 9:
            kodes = 'L' + str(getK)
        else:
            kodes = 'L0' + str(getK)
    else:
        kodes = 'L01'

    paginator = Paginator(sum, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    konteks = {
        'kali': kali,
        'hasilD': hasilD,
        'siswaD': siswaD,
        'kriteriaD': kriteriaD,
        'sum': sum,
        'kodes': kodes,
        'page_obj': page_obj,
    }
    return render(request, 'hasil/index.html', konteks)


@login_required(login_url=settings.LOGIN_URL)
def simpanHasil(request):
    if request.method == 'POST':
        nama = request.POST['nama']
        kode = request.POST['kode']

        hasilD = hasil.objects.all()
        kriteriaD = kriteria.objects.all()
        hasil_dummy1.objects.all().delete()

        lap = laporan_hasil(
            id=kode, nama=nama,
        )
        lap.save()

        nilai_sub1 = 0
        nilai_kriteria1 = 0
        nilai_sub2 = 0
        nilai_kriteria2 = 0
        nilai_sub3 = 0
        nilai_kriteria3 = 0
        nilai_sum = 0

        for i in hasilD:
            siswa_id = i.siswa_id
            if i.kriteria_id == 'C1':
                nilai_sub1 = i.nilai_sub
                # nilai_kriteria1 = i.nilai_kriteria
                nilai_sub2 = 0
                # nilai_kriteria2 = 0
                nilai_sub3 = 0
                # nilai_kriteria3 = 0
            elif i.kriteria_id == 'C2':
                nilai_sub1 = 0
                # nilai_kriteria1 = 0
                nilai_sub2 = i.nilai_sub
                # nilai_kriteria2 = i.nilai_kriteria
                nilai_sub3 = 0
                # nilai_kriteria3 = 0
            elif i.kriteria_id == 'C3':
                nilai_sub1 = 0
                # nilai_kriteria1 = 0
                nilai_sub2 = 0
                # nilai_kriteria2 = 0
                nilai_sub3 = i.nilai_sub
                # nilai_kriteria3 = i.nilai_kriteria
            obj = hasil_dummy1(
                siswa_id=siswa_id, nilai_sub1=nilai_sub1, nilai_sub2=nilai_sub2, nilai_sub3=nilai_sub3
            )
            obj.save()

        jumlah = hasil_dummy1.objects.raw(
            "SELECT 1 id, siswa_id, sum(nilai_sub1) nilai_sub1, sum(nilai_sub2) nilai_sub2, sum(nilai_sub3) nilai_sub3 FROM public.fahp_hasil_dummy1 group by siswa_id ORDER BY siswa_id ASC ")

        for j in jumlah:
            for k in kriteriaD:
                if k.id_kriteria == 'C1':
                    nilai_kriteria1 = k.bobot_kriteria
                elif k.id_kriteria == 'C2':
                    nilai_kriteria2 = k.bobot_kriteria
                elif k.id_kriteria == 'C3':
                    nilai_kriteria3 = k.bobot_kriteria

            nilai_sum = (nilai_kriteria1*j.nilai_sub1) + \
                (nilai_kriteria2*j.nilai_sub2)+(nilai_kriteria3*j.nilai_sub3)
            # print(nilai_sum)
            laporan = laporan_hasil_d(
                laporan_hasil_id=kode, siswa_id=j.siswa_id, nilai_kriteria1=(nilai_kriteria1*j.nilai_sub1), nilai_sub1=j.nilai_sub1, nilai_kriteria2=(nilai_kriteria2*j.nilai_sub2), nilai_sub2=j.nilai_sub2, nilai_kriteria3=(nilai_kriteria3*j.nilai_sub3), nilai_sub3=j.nilai_sub3, nilai_sum=nilai_sum
            )
            laporan.save()

        # obj = laporan_hasil_d(
        #     laporan_hasil_id=kode, siswa_id=siswa_id, nilai_kriteria1=nilai_kriteria1, nilai_sub1=nilai_sub1, nilai_kriteria2=nilai_kriteria2, nilai_sub2=nilai_sub2, nilai_kriteria3=nilai_kriteria3, nilai_sub3=nilai_sub3, nilai_sum=nilai_sum
        # )
        # obj.save()

    return redirect('/fahp/hasil/')
