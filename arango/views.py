import json

from django.http import JsonResponse
from django.shortcuts import render

from django.views import View

from arango.connection import db_conn


class HomeView(View):
    permission_checker = None

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(
            request, self.template_name, context=locals(),
            content_type="text/html", status=200)

    def post(self, request, *args, **kwargs):
        return render(
            request, self.template_name, context=locals(),
            content_type="text/html", status=200)


class Initialize(View):
    permission_checker = None

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        db_conn
        return render(
            request, self.template_name, context=locals(),
            content_type="text/html", status=200)

    def post(self, request, *args, **kwargs):
        return render(
            request, self.template_name, context=locals(),
            content_type="text/html", status=200)


class Provider(View):
    permission_checker = None

    provider_collection = db_conn['provider']

    res = dict()
    res["status"] = False

    def get(self, request, *args, **kwargs):
        all_providers_list = list()

        email = request.GET.get("email")

        if email:
            try:
                ap = self.provider_collection.fetchDocument(key=email)
                data = dict()
                data['name'] = ap["name"]
                data["email"] = ap["email"]
                data["ph_no"] = ap["mobile"]
                data["language"] = ap["language"]
                data["currency"] = ap["currency"]
                all_providers_list.append(data)
            except Exception as e:
                pass

        else:

            all_providers = self.provider_collection.fetchAll()
            for ap in all_providers:
                data = dict()
                data['name'] = ap["name"]
                data["email"] = ap["email"]
                data["ph_no"] = ap["mobile"]
                data["language"] = ap["language"]
                data["currency"] = ap["currency"]
                all_providers_list.append(data)

        return JsonResponse(all_providers_list, safe=False)

    def post(self, request, *args, **kwargs):
        """
        POST data parameters
        # name, email, mobile, language, currency

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        email = request.POST.get("email")
        action = request.POST.get("action")
        if action == "delete":
            try:
                pd = self.provider_collection.fetchDocument(key=email)
                pd.delete()
                self.res["status"] = True
            except Exception as e:
                pass

        else:

            name = request.POST.get("name")
            mobile = request.POST.get("mobile")
            language = request.POST.get("language")
            currency = request.POST.get("currency")
            try:
                pd = self.provider_collection.fetchDocument(key=email)
                if name:
                    pd['name'] = name

                if mobile:
                    pd["ph_no"] = mobile

                if language:
                    pd["language"] = language

                if currency:
                    pd["currency"] = currency

                pd.save()
                self.res["status"] = True

            except Exception as e:

                data = dict()
                data['name'] = name
                data["email"] = email
                data["ph_no"] = mobile
                data["language"] = language
                data["currency"] = currency

                provider_document = self.provider_collection.createDocument()
                provider_document.set(data)
                provider_document._key = email
                provider_document.save()

                self.res["status"] = True

        return JsonResponse(self.res, safe=False)


# create provider
# create service_area
# update provider
# update service_area

class ServiceArea(View):
    """
    provider email, geojson (polygon), polygon_name, price
    """
    permission_checker = None

    service_area_collection = db_conn['service_area']

    res = dict()
    res["status"] = False

    def get(self, request, *args, **kwargs):
        all_providers_list = list()

        email = request.GET.get("email")
        if email:
            try:
                sa = self.service_area_collection.fetchDocument(key=email)
                data = dict()
                data['geojson'] = sa["geojson"]
                data["polygon_name"] = sa["polygon_name"]
                data["price"] = sa["price"]

                all_providers_list.append(data)
            except Exception as e:
                pass
        else:
            all_sa = self.service_area_collection.fetchAll()
            for sa in all_sa:
                data = dict()
                data['geojson'] = sa["geojson"]
                data["email"] = sa._key
                data["polygon_name"] = sa["polygon_name"]
                data["price"] = sa["price"]
                all_providers_list.append(data)

        return JsonResponse(all_providers_list, safe=False)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        action = request.POST.get("action")

        if action == "delete":
            try:
                sa = self.service_area_collection.fetchDocument(key=email)
                sa.delete()
                self.res["status"] = True
            except Exception as e:
                pass

        else:

            geojson = request.POST.get("geojson")
            polygon_name = request.POST.get("polygon_name")
            price = request.POST.get("price")
            try:
                sa = self.service_area_collection.fetchDocument(key=email)
                if geojson:
                    sa['geojson'] = geojson
                if polygon_name:
                    sa["polygon_name"] = polygon_name
                if price:
                    sa["price"] = price

                sa.save()
                self.res["status"] = True

            except Exception as e:

                sa = dict()
                sa['geojson'] = json.loads(geojson)
                sa["polygon_name"] = polygon_name
                sa["price"] = price

                service_document = self.service_area_collection.createDocument()
                service_document.set(sa)
                service_document._key = email
                service_document.save()
                self.res["status"] = True

        return JsonResponse(self.res, safe=False)


class ServiceProvider(View):
    permission_checker = None

    def get(self, request, *args, **kwargs):
        """
        http://127.0.0.1:8000/service-provider/?lat=78.4529560804367&lng=17.4173210167708

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        all_service_providers_list = list()

        lat = request.GET.get("lat")
        lng = request.GET.get("lng")

        t1 = [float(lat), float(lng)]

        target = dict()
        target["type"] = "Polygon"
        target["coordinates"] = [[t1, t1, t1, t1]]

        aql = """
            FOR doc IN service_area
                FILTER GEO_CONTAINS(doc.geojson, @target)
                FOR d1 IN provider
                    FILTER doc._key == d1._key
                RETURN {"name": d1.name, "polygon_name": doc.polygon_name, "price": doc.price, "geojson": doc.geojson}
        """

        # prepare bind data dict
        bind = dict()
        bind["target"] = target

        # execute AQL using AQLQuery method
        query_result = db_conn.AQLQuery(aql, rawResults=True, bindVars=bind)
        for row in query_result:
            all_service_providers_list.append(row)

        # return json data
        return JsonResponse(all_service_providers_list, safe=False)
