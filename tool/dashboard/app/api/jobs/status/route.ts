import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

const PROJECT_ROOT = '/Volumes/Data/gobi-social';
const PRODUCTS_DIR = path.join(PROJECT_ROOT, 'data/products');

export async function POST(req: NextRequest) {
  try {
    const { id, status } = await req.json();
    if (!id || !status) {
      return NextResponse.json({ error: 'Missing id or status' }, { status: 400 });
    }

    const productId = id.replace(/^JOB-/, '');
    const entries = fs.readdirSync(PRODUCTS_DIR, { withFileTypes: true });

    let targetFolder = '';
    for (const entry of entries) {
      if (entry.isDirectory() && entry.name.startsWith(productId)) {
        targetFolder = path.join(PRODUCTS_DIR, entry.name);
        break;
      }
    }

    if (!targetFolder) {
      return NextResponse.json({ error: 'Product folder not found' }, { status: 404 });
    }

    const productJsonPath = path.join(targetFolder, 'product.json');
    let prodData: any = {};
    if (fs.existsSync(productJsonPath)) {
      prodData = JSON.parse(fs.readFileSync(productJsonPath, 'utf-8'));
    }

    prodData.status = status;
    prodData.status_updated_at = new Date().toISOString();
    fs.writeFileSync(productJsonPath, JSON.stringify(prodData, null, 2), 'utf-8');

    return NextResponse.json({ success: true, id, status });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
